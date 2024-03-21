import pytest

from sfdata_schema.spec import Record, TabularSchema
from sfdata_schema.spec.datatypes import DT_STRING


@pytest.fixture
def simple_schema():
    schema =  TabularSchema(id="s1")
    r1 = schema.add_record("r1", label="r1")
    r2 = schema.add_record("r2", label="r2")

    r1.add_field("f1", primary_key=True)
    r1.add_field("f2", primary_key=True)

    r2.add_field("f1", primary_key=True, foreign_keys="r1.f1")
    r2.add_field("f3")

    return schema


def test_schema_structure(simple_schema):
    r1, r2 = simple_schema.records

    assert isinstance(simple_schema, TabularSchema)
    assert isinstance(r1, Record)

    assert r1.id == "r1"
    assert r2.id == "r2"

    fields = r1.fields
    assert len(fields) == 2
    assert fields[0].qname == "r1.f1"
    assert fields[1].qname == "r1.f2"


def test_spec_eq():
    r1 = Record("r1", "r1", [])
    r1_alt = Record("r1", "r1", [])

    r2 = Record("r2", "r2", [])

    assert r1 == r1_alt
    assert r1 != r2


def test_spec_repr():
    r1 = Record("r1", "r1", [])
    assert repr(r1) == "Record(id='r1', options='{}')"

def test_spec_hash():
    r1 = Record("r1", "r1", [])
    r1_alt = Record("r1", "r1", [])

    my_lookup = {
        r1: r1,
        r1_alt: r1_alt
    }

    assert len(my_lookup) == 1
