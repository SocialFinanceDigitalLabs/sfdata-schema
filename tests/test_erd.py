from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from sfdata_schema.spec import TabularSchema
from sfdata_schema.erd import get_erd_context, render_erd


@pytest.fixture
def test_schema():
    schema = TabularSchema(id="person_schema")
    person_record = schema.add_record("person", options={"color": "LightPink"})
    person_record.add_field("id", primary_key=True)
    person_record.add_field("first_name")
    person_record.add_field("last_name")

    pet_record = schema.add_record("pet")
    pet_record.add_field("id", primary_key=True)
    pet_record.add_field("owner_id", foreign_keys=["person.id"])
    pet_record.add_field("name")

    address_record = schema.add_record("address")
    address_record.add_field("owner_id", primary_key=True, foreign_keys=["person.id"])
    address_record.add_field("type", primary_key=True)
    address_record.add_field("address")

    primary_phone_record = schema.add_record("primary_phone")
    primary_phone_record.add_field("id", primary_key=True, foreign_keys=["person.id"])
    primary_phone_record.add_field("number")

    return schema


def test_get_erd_context(test_schema):
    context = get_erd_context(test_schema)
    assert context["schema"] == test_schema

    relationships = context["relationships"]
    assert len(relationships) == 3

    rel_map = {rel.lh: rel for rel in relationships}

    assert rel_map["pet"].lh == "pet"
    assert rel_map["pet"].rh == "person"
    assert rel_map["pet"].lh_c == "0..N"

    assert rel_map["address"].lh == "address"
    assert rel_map["address"].rh == "person"
    assert rel_map["address"].lh_c == "0..N"

    assert rel_map["primary_phone"].lh == "primary_phone"
    assert rel_map["primary_phone"].rh == "person"
    assert rel_map["primary_phone"].lh_c == "0,1"


def test_render_erd(test_schema):
    erd = render_erd(test_schema)
    assert '<TD COLSPAN="3"><B><FONT POINT-SIZE="16">person</FONT></B></TD>' in erd
    assert '<TD ALIGN="LEFT">first_name</TD>'


def create_image(source_image, format, target_path):
    import graphviz
    output_path = graphviz.render("circo", format, source_image)
    output_path = Path(output_path)
    output_path.replace(target_path)
    return target_path


def test_dot(test_schema, dist_dir):
    with TemporaryDirectory() as tmpdir:
        dot_path = Path(tmpdir) / "test.dot"
        with dot_path.open("wt") as file:
            file.write(render_erd(test_schema))

        create_image(dot_path, "png", dist_dir / "test_dot.png")
        svg_path = create_image(dot_path, "svg", dist_dir / "test_dot.svg")

    with svg_path.open("rt") as file:
        svg = file.read()

    assert "<title>person</title>" in svg
    assert "<title>pet</title>" in svg
    assert "<title>address</title>" in svg
    assert '<polygon fill="LightPink"' in svg
