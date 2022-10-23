import pytest

from sfdata_schema import Field, Record, Schema


@pytest.fixture
def simple_schema():
    return Schema(
        records=[
            Record("r1", [Field("f1", primary_key=True), Field("f2")]),
            Record(
                "r2",
                [Field("f1", primary_key=True, foreign_keys=["r1.f1"]), Field("f3")],
            ),
        ]
    )


def test_schema_structure(simple_schema):
    r1 = simple_schema.records["r1"]
    assert r1 is not None
    assert isinstance(r1, Record)
    assert isinstance(r1.schema, Schema)


def test_schema_records(simple_schema):
    assert list(simple_schema.records) == ["r1", "r2"]
    assert len(simple_schema.records) == 2


def test_schema_fields(simple_schema):
    f1 = simple_schema.fields["r1.f1"]
    assert f1.id == "f1"
    assert f1.uid == "r1.f1"

    assert f1.record.schema == simple_schema
    assert list(simple_schema.fields) == ["r1.f1", "r1.f2", "r2.f1", "r2.f3"]
    assert len(simple_schema.fields) == 4


def test_schema_proxy_creation(simple_schema):
    assert isinstance(simple_schema.fields["r1.f2"].record, Record)
    assert isinstance(simple_schema.fields["r1.f2"].record.schema, Schema)


def test_proxy_uninitialized():
    f1 = Field("f1", primary_key=True)
    assert f1.uid == "None.f1"
    assert str(f1.record.id) == "None"


def test_foreign_keys(simple_schema):
    foreign_keys = simple_schema.fields["r2.f1"].foreign_keys
    assert len(foreign_keys) == 1
    assert foreign_keys[0].id == "f1"
    assert foreign_keys[0].uid == "r1.f1"


def test_key_class(simple_schema):
    assert simple_schema.records["r1"].key_class.__name__ == "R1Key"

    key = simple_schema.records["r1"].key_class(f1=1)
    assert key.f1 == 1
    assert key[0] == 1
    assert key.field_values == {"f1": 1}
    assert key.record.id == "r1"

    with pytest.raises(TypeError):
        simple_schema.records["r1"].key_class(f2=1)


def test_record_class(simple_schema):
    assert simple_schema.records["r1"].record_class.__name__ == "R1Record"

    record = simple_schema.records["r1"].record_class(f1=1, f2=2)
    assert record.f1 == 1
    assert record[0] == 1
    assert record.field_values == {"f1": 1, "f2": 2}
    assert record.record.id == "r1"

    assert record.primary_key == (1,)
    assert record.primary_key.field_values == {"f1": 1}

    with pytest.raises(TypeError):
        simple_schema.records["r1"].record_class(f1=1)


def test_standard_types(simple_schema):
    assert len(simple_schema.datatypes) == 10

    assert simple_schema.datatypes["string"].id == "string"
    assert type(simple_schema.datatypes["number"]).__name__ == "Datatype"

    assert simple_schema.fields["r1.f1"].datatype.id == "string"
