from pathlib import Path

import click

from sfdata_schema.parser import parse_schema

from .jekyll import JekyllDocumentationWriter


@click.group()
def docgen():
    pass


@docgen.command()
@click.argument("schema", type=click.Path(exists=True))
@click.argument(
    "output_file", type=click.Path(file_okay=True, dir_okay=False), metavar="OUTPUT"
)
def graphviz(schema, output_file):
    """Generate an entity relationship diagram using graphviz."""
    from .erd import graphviz_render_erd

    schema = Path(schema)
    output_file = Path(output_file)

    print(f"Generating ERD diagram for {schema} and writing to {output_file}")

    spec = parse_schema(schema)

    image_format = output_file.suffix[1:].lower()
    graphviz_render_erd(spec, image_format, output_file)


@docgen.command()
@click.argument("schema", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path(file_okay=False), metavar="OUTPUT")
@click.option("--erd", is_flag=True, help="Also generate an ERD diagram")
def jekyll(schema, output_dir, erd):
    """Generate Jekyll documentation."""
    schema = Path(schema)
    output_dir = Path(output_dir)

    print(f"Generating Jekyll documentation for {schema} and writing to {output_dir}")

    spec = parse_schema(schema)

    writer = JekyllDocumentationWriter(output_dir)
    writer.copy_templates()
    writer.write_all_collections(spec)
    writer.write_all_data(spec)

    if erd:
        include_dir = output_dir / "_includes"
        include_dir.mkdir(parents=True, exist_ok=True)
        erd_file = include_dir / "erd.svg"

        svg_content = writer.generate_embeddable_erd(spec)
        erd_file.write_bytes(svg_content)

        print(f"Generated ERD diagram in {erd_file}")
        print(
            " To include the ERD diagram in your Jekyll site, you will have to manually update 'erd_include: true' to _config.yml"
        )
