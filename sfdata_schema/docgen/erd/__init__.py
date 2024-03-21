from collections import namedtuple
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping, Optional, Union

from sfdata_schema.spec import TabularSchema

Relationship = namedtuple("Relationship", "lh rh lh_c rh_c")


def get_erd_context(schema: TabularSchema) -> Mapping[str, Any]:
    relationships = []

    for r in schema.records:
        pk = [p.id for p in r.primary_keys]
        for f in r.fields:
            if f.foreign_keys:
                for fk in f.foreign_keys:
                    lh_c = "0,1" if pk == [f.id] else "0..N"
                    relationships.append(
                        Relationship(lh=r.id, rh=fk.record.id, lh_c=lh_c, rh_c=1)
                    )

    return dict(schema=schema, relationships=relationships)


def render_erd(
    schema: TabularSchema,
    template_name: str = "erd.dot",
    template_path: Union[str, Path] = None,
) -> str:
    try:
        from jinja2 import Environment, FileSystemLoader, select_autoescape
    except ImportError:
        raise ImportError("This function requires the jinja2 package")

    if template_path is None:
        template_path = Path(__file__).parent / "templates"

    env = Environment(
        loader=FileSystemLoader(template_path), autoescape=select_autoescape()
    )

    context = get_erd_context(schema)
    template = env.get_template(template_name)
    return template.render(context)


def graphviz_render_erd(
    schema: TabularSchema, format: str = "png", target_path: Path = None, **kwargs
) -> Optional[bytes]:
    import graphviz

    with TemporaryDirectory() as tmpdir:
        dot_path = Path(tmpdir) / "graph.dot"
        with dot_path.open("wt") as file:
            file.write(render_erd(schema, **kwargs))

        output_path = graphviz.render("circo", format, dot_path)
        output_path = Path(output_path)

        if target_path:
            output_path.replace(target_path)
            data = None
        else:
            data = output_path.read_bytes()

    return data
