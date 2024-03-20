import pytest

from sfdata_schema.spec import Field, Record, TabularSchema, Datatype


@pytest.fixture
def simple_schema():
    dt1 = Datatype("str")
    r1_f1 = Field("r1.f1", label="f1", datatype=str, primary_key=True)
    r1_f2 = Field("r1.f2", label="f2", datatype=str)
    r2_f1 = Field("r2.f1", label="f1", datatype=str, primary_key=True, foreign_keys=[r1_f1])
    r2_f3 = Field("r2.f3", label="f3", datatype=str)

    r1 = Record("r1", "r1", [r1_f1, r1_f2])
    r2 = Record("r2", "r2", [r2_f1, r2_f3])

    return TabularSchema(id="s1", records=[r1, r2])


def test_schema_structure(simple_schema):
    r1, r2 = simple_schema.records

    assert isinstance(simple_schema, TabularSchema)
    assert isinstance(r1, Record)

    assert r1.id == "r1"
    assert r2.id == "r2"

    fields = r1.fields
    assert len(fields) == 2
    assert fields[0].id == "r1.f1"
    assert fields[1].id == "r1.f2"


def test_spec_eq():
    r1 = Record("r1", "r1", [])
    r1_alt = Record("r1", "r1", [])

    r2 = Record("r2", "r2", [])

    assert r1 == r1_alt
    assert r1 != r2


def test_spec_repr():
    r1 = Record("r1", "r1", [])
    assert repr(r1) == "sfdata_schema.spec._data.Record(id='r1', label='r1', fields=[], description=None, options={})"

def test_spec_hash():
    r1 = Record("r1", "r1", [])
    r1_alt = Record("r1", "r1", [])

    my_lookup = {
        r1: r1,
        r1_alt: r1_alt
    }

    assert len(my_lookup) == 1
