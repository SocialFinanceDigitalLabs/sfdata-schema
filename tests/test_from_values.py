from sfdata_schema import Record, Schema


def test_field_from_string():
    schema = Schema(records=[Record("person", ["*id", "first_name", "last_name"])])
    assert schema.fields["person.id"].id == "id"
    assert schema.fields["person.id"].primary_key
    assert schema.fields["person.first_name"].schema == schema

    assert schema.fields["person.first_name"].id == "first_name"
    assert not schema.fields["person.first_name"].primary_key

    assert list(schema.fields) == ["person.id", "person.first_name", "person.last_name"]


def test_field_from_dict():
    schema = Schema(
        records=[
            Record(
                "person",
                [
                    {"id": "id", "primary_key": True},
                    {"id": "first_name"},
                    {"id": "last_name"},
                ],
            )
        ]
    )

    assert schema.fields["person.id"].id == "id"
    assert schema.fields["person.id"].primary_key
    assert schema.fields["person.first_name"].schema == schema

    assert schema.fields["person.first_name"].id == "first_name"
    assert not schema.fields["person.first_name"].primary_key

    assert list(schema.fields) == ["person.id", "person.first_name", "person.last_name"]


def test_field_with_extras():
    schema = Schema(
        records=[
            Record(
                "person",
                [
                    {"id": "id", "primary_key": True, "description": "The person's ID"},
                ],
            )
        ]
    )
    assert schema.fields["person.id"].extras["description"] == "The person's ID"
