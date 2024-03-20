from . import Datatype

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
