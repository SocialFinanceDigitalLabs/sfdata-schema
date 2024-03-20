from dataclasses import dataclass, field, make_dataclass
from enum import Enum
from typing import Any, List, Mapping, Optional


def schemaitem(cls=None, /, *args, **kwargs):
    """
    Schema items are the building blocks of a schema. They are the equivalent of the classes in the schema. This
    """

    def wrap(cls):
        # Define the 'id' field as a required field
        fields = [("id", str, field(hash=True))]

        # Add the original fields from the class
        cls = dataclass(cls)
        fields += [(f.name, f.type, f) for f in cls.__dataclass_fields__.values()]

        # Append 'description' and 'options' field as the last field with a default value
        fields.append(
            ("description", Optional[str], field(default=None)),
        )
        fields.append(
            ("options", Optional[Mapping[str, Any]], field(default_factory=dict))
        )

        # Exclude all but ID from equality comparison
        for f in fields[1:]:
            f[2].compare = False

        # Set the default values for the dataclass
        kwargs.setdefault("eq", True)
        kwargs.setdefault("frozen", True)
        kwargs.setdefault("repr", True)

        # Create a new dataclass with the extended fields
        full_name = cls.__module__ + "." + cls.__qualname__
        return make_dataclass(full_name, fields, **kwargs)

    if cls is None:
        return wrap

    return wrap(cls)

class WhitespaceRestriction(Enum):
    PRESERVE = "preserve"
    REPLACE = "replace"
    COLLAPSE = "collapse"

@dataclass
class DatatypeRestriction:
    """A restriction on a datatype. For example the length of a string or the range of a number.
    These restrictions are based on the XML Schema Part 2: Datatypes.
    """

    # Specifies the lower bounds for numeric values (the value is exclusive)
    min_exclusive: int = None

    # Specifies the lower bounds for numeric values (the value is inclusive)
    min_inclusive: int = None

    # Specifies the upper bounds for numeric values (the value is exclusive)
    max_exclusive: int = None

    # Specifies the upper bounds for numeric values (the value is inclusive)
    max_inclusive: int = None

    # Specifies the total number of digits that are allowed
    total_digits: int = None

    # Specifies the maximum number of fractional digits that are allowed
    fraction_digits: int = None
 
    # Specifies the exact length of a string
    length: int = None
 
    # Specifies the minimum length of a string
    min_length: int = None

    # Specifies the maximum length of a string
    max_length: int = None

    # Specifies a pattern for a string
    pattern: str = None

    # Specifies a list of valid values for a field
    enumeration: List[str] = None

    # Specifies how white space (line feeds, tabs, spaces, and carriage returns) is handled
    white_space: WhitespaceRestriction = None



@schemaitem(eq=True)
class Datatype:
    """A datatype is a type of data that can be stored in a field. Implementations can chose to extend
    the standard datatypes with custom ones. The standard datatypes however are based on the XML Schema Part"""

    extends: "Datatype" = None
    restriction: DatatypeRestriction = None

@schemaitem
class CategoricalValueItem:
    """
    A valid value for a categorical field. The 'id' is the expected value and the 'label' is the human readable
    representation of the value.
    """

    label: str


@schemaitem
class CategoricalValueType:
    """
    A datatype for categorical fields. The 'categories' attribute is a list of valid values for the field.
    """

    categories: List[CategoricalValueItem]


@schemaitem
class Field:
    """
    A field is a single columns in a table or element in a record. It has a label and a datatype. The identifier has to
    be unique within the schema. The label is the entry as used in the data, for example the column header or the
    element name.
    """

    label: str
    datatype: Datatype
    primary_key: bool = False
    foreign_keys: List[str] = None


@schemaitem
class Record:
    """
    A record is a collection of fields. It is the equivalent of a table in a database or a row in a CSV file.

    The identifier has to be unique within the schema. The label is the entry as used in the data, for example
    the table or sheet name.
    """

    label: str
    fields: List[Field]


@schemaitem
class TabularSchema:
    """
    A tabular schema is a collection of datatypes and records. It is the equivalent of a database schema, Excel file
    with multiple sheets or a collection of CSV files.
    """

    records: List[Record]
