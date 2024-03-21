from dataclasses import dataclass, field
from typing import Any, List, Literal, Mapping, Optional


@dataclass(frozen=True, eq=True, repr=True)
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
    white_space: Literal["preserve", "replace", "collapse"] = None


@dataclass(frozen=True, eq=True, repr=True)
class Datatype:
    """A datatype is a type of data that can be stored in a field. Implementations can chose to extend
    the standard datatypes with custom ones. The standard datatypes however are based on the XML Schema Part"""

    id: str
    description: Optional[str] = field(default=None, compare=False)
    extends: "Datatype" = field(default=None, compare=False)
    restriction: DatatypeRestriction = field(default=None, compare=False)
    options: Optional[Mapping[str, Any]] = field(default=None, compare=False)


DT_STRING = Datatype("string")
DT_INTEGER = Datatype("integer")
DT_NUMBER = Datatype("number")
DT_BOOLEAN = Datatype("boolean")
DT_DATE = Datatype("date")
DT_TIME = Datatype("time")
DT_DATETIME = Datatype("datetime")
DT_YEAR = Datatype("year")
DT_YEARMONTH = Datatype("yearmonth")
DT_MONTHDAY = Datatype("monthday")

STANDARD_TYPES = (
    DT_STRING,
    DT_INTEGER,
    DT_NUMBER,
    DT_BOOLEAN,
    DT_DATE,
    DT_TIME,
    DT_DATETIME,
    DT_YEAR,
    DT_YEARMONTH,
    DT_MONTHDAY,
)
