from pathlib import Path
from typing import Any, Dict, Iterable, List, Protocol, Union, runtime_checkable
from dataclasses import fields

import json5
import yaml

from sfdata_schema import spec
from sfdata_schema.spec.datatypes import STANDARD_TYPES, Datatype, DatatypeRestriction


@runtime_checkable
class Readable(Protocol):
    def read(self) -> str:
        ...


ParserInput = Union[Dict[str, Any], Readable, str, Path]

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
    records = schema.pop("records", {})
    if "id" not in schema:
        schema["id"] = "unknown"

    schema = spec.TabularSchema(**schema, datatypes=datatypes)
    for id, record in records.items():
        if "id" not in record:
            record["id"] = id
        parse_record(schema, record)

    return schema


def _parse_file(path: Path) -> spec.TabularSchema:
    with path.open("rt") as f:
        return _parse_string(f.read())


def _parse_string(content: str) -> spec.TabularSchema:
    if content.startswith("{"):
        content = json5.loads(content)
    else:
        content = yaml.safe_load(content)
    return _parse_dict(content)


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
        datatype["restriction"] = DatatypeRestriction(**datatype["restriction"])

    return Datatype(**datatype)


def parse_datatypes(datatypes: Dict[str, Dict[str, str]]) -> List[spec.Datatype]:
    datatype_list = list(STANDARD_TYPES)
    for id, datatype in datatypes.items():
        if "id" not in datatype:
            datatype["id"] = id
        dt = parse_datatype(datatype, datatype_list)
        datatype_list.append(dt)
    return datatype_list


def parse_record(
    schema: spec.TabularSchema, record: Dict[str, Any]
) -> spec.Record:
    fields = record.pop("fields") or {}

    schema_record = schema.add_record(**record)
    for id, field in fields.items():
        if "id" not in field:
            field["id"] = id
        schema_record.add_field(**field)
            
    return schema_record



