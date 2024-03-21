from sfdata_schema.parser import parse_datatype, parse_datatypes
from sfdata_schema.spec.datatypes import DT_STRING, STANDARD_TYPES


def test_parse_datatype():
    data = {"id": "testtype1", "description": "This is a test type"}
    dt = parse_datatype(data)
    assert dt.id == "testtype1"
    assert dt.description == "This is a test type"


def test_parse_datatype_extends():
    data = {
        "id": "testtype1",
        "description": "This is a test type",
        "extends": "string",
        "restriction": {"enumeration": ["a", "b", "c"]},
    }
    dt = parse_datatype(data, STANDARD_TYPES)
    assert dt.id == "testtype1"
    assert dt.extends == DT_STRING
    assert dt.restriction.enumeration == ["a", "b", "c"]


def test_parse_datatypes():
    data = {"testtype1": {"description": "This is a test type"}}
    dt = parse_datatypes(data)
    assert len(dt) == len(STANDARD_TYPES) + 1
    assert dt[-1].id == "testtype1"
    assert dt[-1].description == "This is a test type"


def test_parse_datatypes_with_id():
    data = {
        "testtype1": {
            "id": "customtype",
            "description": "This is a test type with a specific ID",
        }
    }
    dt = parse_datatypes(data)
    assert dt[-1].id == "customtype"
    assert dt[-1].description == "This is a test type with a specific ID"


def test_parse_datatypes_extends():
    data = {
        "testtype1": {"description": "This is a test type", "extends": "string"},
        "testtype2": {"description": "This is a test type", "extends": "testtype1"},
    }
    dt = parse_datatypes(data)
    assert len(dt) == len(STANDARD_TYPES) + 2

    dt_map = {d.id: d for d in dt}
    assert dt_map["testtype1"].extends == DT_STRING
    assert dt_map["testtype2"].extends == dt_map["testtype1"]
