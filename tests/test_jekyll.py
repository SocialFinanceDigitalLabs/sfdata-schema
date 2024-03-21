from pathlib import Path

import yaml

from sfdata_schema.docgen.jekyll import JekyllDocumentationWriter


def test_write_field_data(pet_schema, tmpdir):
    tmpdir = Path(tmpdir)
    writer = JekyllDocumentationWriter(tmpdir)
    data_file = writer.write_field_data(pet_schema)

    field_data = yaml.safe_load(data_file.read_text())

    assert set(f["qname"] for f in field_data) == {
        "person.id",
        "person.first_name",
        "person.last_name",
        "pet.id",
        "pet.owner_id",
        "pet.name",
        "address.owner_id",
        "address.type",
        "address.address",
        "primary_phone.id",
        "primary_phone.number",
    }


def test_write_record_data(pet_schema, tmpdir):
    tmpdir = Path(tmpdir)
    writer = JekyllDocumentationWriter(tmpdir)
    data_file = writer.write_record_data(pet_schema)

    record_data = yaml.safe_load(data_file.read_text())

    assert set(r["id"] for r in record_data) == {
        "person",
        "pet",
        "address",
        "primary_phone",
    }
