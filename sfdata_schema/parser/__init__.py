from pathlib import Path
from typing import Any, Dict, Iterable, List, Protocol, Union, runtime_checkable
from dataclasses import fields

import jstyleson
import yaml

from sfdata_schema import spec
from sfdata_schema.spec.datatypes import DT_STRING, STANDARD_TYPES


@runtime_checkable
class Readable(Protocol):
    def read(self) -> str:
        ...


ParserInput = Union[Dict[str, Any], Readable, str, Path]


def parse_datatype(
    datatype: Dict[str, Any], datatypes: Iterable[spec.Datatype] = None
) -> spec.Datatype:
    if "extends" in datatype:
        if datatypes is None:
            raise ValueError("Cannot extend a datatype without a list of datatypes")

        extends = next((dt for dt in datatypes if dt.id == datatype["extends"]), None)
        if extends is None:
            raise ValueError(
                f"Cannot find datatype {datatype['extends']} to extend from"
            )

        datatype["extends"] = extends

    if "restriction" in datatype:
        datatype["restriction"] = spec.DatatypeRestriction(
            **datatype["restriction"]
        )

    return spec.Datatype(**datatype)


def parse_datatypes(datatypes: Dict[str, Dict[str, str]]) -> List[spec.Datatype]:
    datatype_list = list(STANDARD_TYPES)
    for id, datatype in datatypes.items():
        if "id" not in datatype:
            datatype["id"] = id
        dt = parse_datatype(datatype, datatype_list)
        datatype_list.append(dt)
    return datatype_list

def parse_fields(fields: Dict[str, Any], datatypes: Iterable[spec.Datatype] = None) -> List[spec.Field]:
    field_list = []
    for id, field in fields.items():
        if "id" not in field:
            field["id"] = id
        if "label" not in field:
            field["label"] = field["id"]
        if "datatype" not in field:
            field["datatype"] = DT_STRING
        field_list.append(parse_field(field, datatypes))
    return field_list
        
def parse_field(field: Dict[str, Any], datatypes: Iterable[spec.Datatype] = None) -> spec.Field:
    if "datatype" in field and datatypes is not None:
        field["datatype"] = next((dt for dt in datatypes if dt.id == field["datatype"]), None)
    return spec.Field(**field)

def parse_records(records: Dict[str, Any], datatypes: Iterable[spec.Datatype] = None) -> List[spec.Record]:
    record_list = []
    for id, record in records.items():
        if "id" not in record:
            record["id"] = id
        if "label" not in record:
            record["label"] = record["id"]
        record_list.append(parse_record(record, datatypes))
    return record_list

def parse_record(record: Dict[str, Any], datatypes: Iterable[spec.Datatype] = None) -> spec.Record:
    record["fields"] = parse_fields(record.get("fields", {}), datatypes)
    return spec.Record(**record)


def parse_schema(schema: ParserInput) -> spec.TabularSchema:
    if isinstance(schema, dict):
        return _parse_dict(schema)
    elif isinstance(schema, Readable):
        return _parse_string(schema.read())
    elif isinstance(schema, str):
        return _parse_file(Path(str))
    elif isinstance(schema, Path):
        return _parse_file(schema)
    

def _parse_dict(schema: Dict[str, Any]) -> spec.TabularSchema:
    datatypes = parse_datatypes(schema.pop("datatypes", {}))
    schema["records"] = parse_records(schema.get("records", {}), datatypes)
    schema.setdefault("options", {})

    if "id" not in schema:
        schema["id"] = "unknown"

    schema_fields = [f.name for f in fields(spec.TabularSchema)]
    for key in list(schema.keys()):
        if key not in schema_fields:
            schema["options"][key] = schema.pop(key)

    return spec.TabularSchema(**schema)


def _parse_file(path: Path) -> spec.TabularSchema:
    with path.open("rt") as f:
        return _parse_string(f.read())


def _parse_string(content: str) -> spec.TabularSchema:
    if content.startswith("{"):
        content = jstyleson.loads(content)
    else:
        content = yaml.safe_load(content)
    return _parse_dict(content)


