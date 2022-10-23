from pathlib import Path

from sfdata_schema import Schema
from sfdata_schema.parser import parse_schema


def test_parse_single_file_yaml():
    """Test parsing a single file."""

    file = Path(__file__).parent / "fixtures" / "single-file-schema.yml"
    assert_schema(file)


def test_parse_single_file_json():
    """Test parsing a single file."""

    file = Path(__file__).parent / "fixtures" / "single-file-schema.json"
    assert_schema(file)


def assert_schema(file):
    schema = parse_schema(file)

    assert isinstance(schema, Schema)

    assert len(schema.records) == 2
    assert list(schema.fields) == [
        "person.id",
        "person.name",
        "address.person_id",
        "address.type",
        "address.street",
        "address.city",
        "address.postal_code",
    ]

    assert schema.fields["person.id"].primary_key
    assert not schema.fields["person.name"].primary_key
    assert schema.fields["address.person_id"].primary_key

    assert len(schema.fields["address.person_id"].foreign_keys) == 1
    assert (
        schema.fields["address.person_id"].foreign_keys[0] == schema.fields["person.id"]
    )
