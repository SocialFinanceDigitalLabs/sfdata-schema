from pathlib import Path
from sfdata_schema.spec import TabularSchema
from sfdata_schema.parser import parse_schema, Readable

def test_readable():
    from io import StringIO

    readable = StringIO("{'bar': 1}")
    assert isinstance(readable, Readable)

    not_readable = {"bar": 1}
    assert not isinstance(not_readable, Readable)


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

    assert isinstance(schema, TabularSchema)

    assert len(schema.records) == 2

    all_fields = {f"{r.id}.{f.id}": f for r in schema.records for f in r.fields}

    assert list(all_fields) == [
        "person.id",
        "person.name",
        "address.person_id",
        "address.type",
        "address.street",
        "address.city",
        "address.postal_code",
    ]

    assert all_fields["person.id"].primary_key
    assert not all_fields["person.name"].primary_key
    assert all_fields["address.person_id"].primary_key

    assert len(all_fields["address.person_id"].foreign_keys) == 1
    assert all_fields["address.person_id"].foreign_keys[0] == "person.id"
    