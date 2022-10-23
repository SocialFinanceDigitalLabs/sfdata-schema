from collections import namedtuple
from pathlib import Path
from typing import Any, Mapping, Union

from jinja2 import Environment, FileSystemLoader, select_autoescape

from sfdata_schema import Schema

Relationship = namedtuple("Relationship", "lh rh lh_c rh_c")


def get_erd_context(schema: Schema) -> Mapping[str, Any]:
    relationships = []

    for r in schema.records.values():
        pk = r.primary_keys
        for f in r.fields:
            if f.foreign_keys:
                for fk in f.foreign_keys:
                    lh_c = "0,1" if pk == [f] else "0..N"
                    relationships.append(
                        Relationship(lh=r.id, rh=fk.record.id, lh_c=lh_c, rh_c=1)
                    )

    return dict(schema=schema, relationships=relationships)


def render_erd(
    schema: Schema,
    template_name: str = "erd.dot",
    template_path: Union[str, Path] = None,
):
    if template_path is None:
        template_path = Path(__file__).parent / "templates"

    env = Environment(
        loader=FileSystemLoader(template_path), autoescape=select_autoescape()
    )

    context = get_erd_context(schema)
    template = env.get_template(template_name)
    return template.render(context)
