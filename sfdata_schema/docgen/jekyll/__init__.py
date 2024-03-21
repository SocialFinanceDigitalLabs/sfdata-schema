import xml.etree.ElementTree as ET
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict

import yaml

from sfdata_schema.spec import Field, Record
from sfdata_schema.spec import TabularSchema as Specification
from sfdata_schema.spec.datatypes import Datatype


def _remove_nulls(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


def _write__with_frontmatter(content: str, **frontmatter) -> str:
    fm = yaml.dump(frontmatter, sort_keys=False)
    return f"---\n{fm}---\n{content}"


class JekyllDocumentationWriter:

    def __init__(
        self,
        jekyll_dir: Path,
        data_prefix: str = "_data",
        collection_prefix: str = "",
    ):
        self.jekyll_dir = jekyll_dir
        self.collection_prefix = collection_prefix
        self.data_prefix = data_prefix

    def datatype_to_dict(self, datatype: Datatype) -> Dict[str, Any]:
        data = {
            "id": datatype.id,
            "description": datatype.description,
            "extends": (
                self.datatype_to_dict(datatype.extends) if datatype.extends else None
            ),
            "options": datatype.options,
            "restriction": (
                _remove_nulls(asdict(datatype.restriction))
                if datatype.restriction
                else None
            ),
        }
        return _remove_nulls(data)

    def field_to_dict(self, field: Field) -> Dict[str, Any]:
        data = {
            "id": field.id,
            "qname": field.qname,
            "record": field.record.id,
            "label": field.label,
            "description": field.description,
            "datatype": self.datatype_to_dict(field.datatype),
            "primary_key": field.primary_key,
            "foreign_keys": [f.qname for f in field.foreign_keys],
            "options": field.options,
        }
        return _remove_nulls(data)

    def record_to_dict(self, record: Record) -> Dict[str, Any]:
        return {
            "id": record.id,
            "label": record.label,
            "description": record.description,
            "options": record.options,
            "fields": [self.field_to_dict(f) for f in record.fields],
        }

    def write_record_data(self, spec: Specification) -> Path:
        dir = self.jekyll_dir / self.data_prefix
        dir.mkdir(parents=True, exist_ok=True)
        data_file = dir / "records.yml"

        with open(data_file, "wt") as file:
            record_data = [self.record_to_dict(r) for r in spec.records]
            yaml.dump(record_data, file, sort_keys=False)

        return data_file

    def write_field_data(self, spec: Specification) -> Path:
        dir = self.jekyll_dir / self.data_prefix
        dir.mkdir(parents=True, exist_ok=True)
        data_file = dir / "fields.yml"

        with open(data_file, "wt") as file:
            field_data = [self.field_to_dict(f) for f in spec.all_fields]
            yaml.dump(field_data, file, sort_keys=False)

        return data_file

    def write_datatypes_data(self, spec: Specification, only_used=True) -> Path:
        dir = self.jekyll_dir / self.data_prefix
        dir.mkdir(parents=True, exist_ok=True)
        data_file = dir / "datatypes.yml"

        with open(data_file, "wt") as file:
            datatypes = spec.used_datatypes if only_used else spec.datatypes
            datatype_data = [self.datatype_to_dict(d) for d in datatypes]
            yaml.dump(datatype_data, file, sort_keys=False)

        return data_file

    def write_record_collection(self, spec: Specification) -> Path:
        dir = self.jekyll_dir / self.collection_prefix / "_records"
        dir.mkdir(parents=True, exist_ok=True)

        for r in spec.records:
            data_file = dir / f"{r.id}.md"
            data_file.write_text(
                _write__with_frontmatter(
                    "", layout="record", record_id=r.id, spec=self.record_to_dict(r)
                )
            )

        return dir

    def write_field_collection(self, spec: Specification) -> Path:
        dir = self.jekyll_dir / self.collection_prefix / "_fields"
        dir.mkdir(parents=True, exist_ok=True)

        for f in spec.all_fields:
            data_file = dir / f"{f.qname}.md"
            data_file.write_text(
                _write__with_frontmatter(
                    "",
                    layout="field",
                    field_id=f.id,
                    record_id=f.record.id,
                    field_qname=f.qname,
                    spec=self.field_to_dict(f),
                )
            )

        return dir

    def write_datatype_collection(self, spec: Specification, only_used=True) -> Path:
        dir = self.jekyll_dir / self.collection_prefix / "_datatypes"
        dir.mkdir(parents=True, exist_ok=True)

        datatypes = spec.used_datatypes if only_used else spec.datatypes

        for d in datatypes:
            data_file = dir / f"{d.id}.md"
            data_file.write_text(
                _write__with_frontmatter(
                    "",
                    layout="datatype",
                    datatype_id=d.id,
                    spec=self.datatype_to_dict(d),
                )
            )

        return dir

    def write_all_collections(self, spec: Specification) -> None:
        self.write_record_collection(spec)
        self.write_field_collection(spec)
        self.write_datatype_collection(spec)

    def write_all_data(self, spec: Specification) -> None:
        self.write_record_data(spec)
        self.write_field_data(spec)
        self.write_datatypes_data(spec)

    def copy_templates(self, template_dir: Path = None) -> None:
        if template_dir is None:
            template_dir = Path(__file__).parent / "templates/jekyll"

        # Find all files in this folder and copy them recursively to the output folder
        # Don't overwrite existing files
        for f in template_dir.rglob("*"):
            if f.is_file():
                dest = self.jekyll_dir / f.relative_to(template_dir)
                if not dest.exists():
                    print(f"Copying {f} to {dest}")
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_text(f.read_text())
                else:
                    print(f"Skipping {dest} because it already exists")

    def generate_embeddable_erd(
        self, spec: Specification, link_pattern="/records/{record_id}.html"
    ):
        """
        This function generates an embeddable ERD diagram for the Jekyll site. It's a bit of a hack and is quite dependent on graphviz creating
        the same SVG structure every time. It's also not very efficient, as it reads the SVG file into memory and then writes it out again.

        However, it's a start and it works for now.
        """
        from sfdata_schema.docgen.erd import graphviz_render_erd

        namespaces = {"svg": "http://www.w3.org/2000/svg"}
        ET.register_namespace("", "http://www.w3.org/2000/svg")

        svg_content = graphviz_render_erd(spec, "svg")

        root = ET.fromstring(svg_content)
        root.attrib["width"] = "auto"
        root.attrib["height"] = "auto"

        root_graph = root.find("svg:g", namespaces)
        background = root_graph.find("svg:polygon", namespaces)
        root_graph.remove(background)

        sub_graphs = root_graph.findall("svg:g", namespaces)
        for sg in sub_graphs:
            if sg.attrib["class"] != "node":
                continue
            root_graph.remove(sg)

            filename = link_pattern.format(record_id=sg.attrib["id"])
            link = ET.Element("a")
            link.attrib["href"] = "{{ '" + filename + "' | relative_url }}"
            root_graph.append(link)
            link.append(sg)

        return ET.tostring(root, encoding="utf-8")

    # def write_gitinfo():
    #     dir = jekyll_dir / "_data"
    #     dir.mkdir(parents=True, exist_ok=True)
    #     with open(dir / "git.yml", "wt") as file:
    #         yaml.dump(get_git_data(), file)
