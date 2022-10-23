from pathlib import Path
from typing import Any, Dict

import jstyleson
import yaml

from sfdata_schema import Field, Record, Schema


def parse_schema(schema) -> Schema:
    if isinstance(schema, dict):
        return Schema.from_value(schema)
    elif hasattr(schema, "read"):
        return _parse_string(schema.read())
    else:
        return _parse_file(schema)


def _parse_file(path) -> Schema:
    path = Path(path)
    with path.open("rt") as f:
        return _parse_string(f.read())


def _parse_string(content) -> Schema:
    if content.startswith("{"):
        content = jstyleson.loads(content)
    else:
        content = yaml.safe_load(content)
    return Schema.from_value(content)
