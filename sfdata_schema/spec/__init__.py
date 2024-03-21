from typing import Any, Iterable, List, Mapping, Optional, Tuple

from .datatypes import DT_STRING, STANDARD_TYPES, Datatype


class __FieldSummary__:
    """A helper class to generate a string representation of the fields of an object. This is used to generate the
    __repr__ method for the schema items."""

    def __init__(self, include_none=False):
        self.include_none = include_none
        self.fields = []

    def add_field(self, obj, field):
        if hasattr(obj, field):
            self.add_value(field, getattr(obj, field))
        elif field in obj:
            self.add_value(field, obj[field])
        else:
            raise AttributeError(f"Object has no attribute '{field}'")

    def add_value(self, field, value):
        if self.include_none or value is not None:
            self.fields.append((field, value))

    def as_string(self):
        return ", ".join([f"{field}='{value}'" for field, value in self.fields])


class SchemaItem:
    """Base class for all schema items. This class is used to define the common attributes and methods for all schema
    items.
    """

    def __init__(
        self,
        id: str,
        schema: "Schema",
        description: Optional[str] = None,
        options: Optional[Mapping[str, Any]] = None,
    ):
        self._id = id
        self._schema = schema
        self._description = description
        self._options = options or {}

    @property
    def id(self) -> str:
        return self._id

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def options(self) -> Mapping[str, Any]:
        return self._options

    @property
    def schema(self) -> "Schema":
        return self._schema

    def __eq__(self, other):
        if not isinstance(other, SchemaItem):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr_fields__(self):
        fields = __FieldSummary__(include_none=False)
        fields.add_field(self, "id")
        fields.add_field(self, "description")
        fields.add_field(self, "options")
        return fields

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__repr_fields__().as_string()})"


class CategoricalValueItem(SchemaItem):
    """
    A valid value for a categorical field. The 'id' is the expected value and the 'label' is the human readable
    representation of the value.
    """

    def __init__(
        self,
        id: str,
        schema: "Schema",
        label: str,
        description: Optional[str] = None,
        options: Optional[Mapping[str, Any]] = None,
    ):
        super().__init__(id, schema, description, options)
        self._label = label


class CategoricalValueType(Datatype):
    """
    A datatype for categorical fields. The 'categories' attribute is a list of valid values for the field.
    """

    def __init__(
        self,
        id: str,
        schema: "Schema",
        description: Optional[str] = None,
        options: Optional[Mapping[str, Any]] = None,
        extends: "Datatype" = None,
        categories: Tuple[CategoricalValueItem] = None,
    ):
        super().__init__(id, schema, description, options, extends)
        self._categories = categories


class Field(SchemaItem):
    """
    A field is a single columns in a table or element in a record. It has a label and a datatype. The identifier has to
    be unique within the schema. The label is the entry as used in the data, for example the column header or the
    element name.
    """

    def __init__(
        self,
        id: str,
        record: "Record",
        label: str,
        datatype: "Datatype",
        primary_key: bool = False,
        foreign_keys: Optional[List[str]] = None,
        description: Optional[str] = None,
        options: Optional[Mapping[str, Any]] = None,
    ):
        super().__init__(id, record.schema, description, options)
        self._record = record
        self._label = label or id
        self._datatype = record.schema.get_datatype(datatype)
        self._primary_key = primary_key
        self._foreign_keys = foreign_keys or tuple()

    @property
    def record(self) -> "Record":
        return self._record

    @property
    def schema(self) -> "Schema":
        return self.record.schema

    @property
    def qname(self) -> str:
        return f"{self.record.id}.{self.id}"

    @property
    def label(self) -> str:
        return self._label

    @property
    def datatype(self) -> "Datatype":
        return self._datatype

    @property
    def primary_key(self) -> bool:
        return self._primary_key

    @property
    def foreign_keys(self) -> Tuple["Field"]:
        return tuple(self.schema.get_field(fk) for fk in self._foreign_keys)

    @property
    def foreign_key_names(self) -> Tuple[str]:
        return tuple(self._foreign_keys)


class Record(SchemaItem):
    """
    A record is a collection of fields. It is the equivalent of a table in a database or a row in a CSV file.

    The identifier has to be unique within the schema. The label is the entry as used in the data, for example
    the table or sheet name.
    """

    def __init__(
        self,
        id: str,
        schema: "Schema",
        label: str,
        description: Optional[str] = None,
        options: Optional[Mapping[str, Any]] = None,
    ):
        super().__init__(id, schema, description, options)
        self._label = label
        self._fields = []

    @property
    def schema(self) -> "Schema":
        return self._schema

    @property
    def label(self) -> str:
        return self._label

    def add_field(
        self,
        id: str,
        label: str = None,
        datatype: "Datatype" = DT_STRING,
        primary_key: bool = False,
        foreign_keys: Optional[List[str]] = None,
        description: Optional[str] = None,
        options: Optional[Mapping[str, Any]] = None,
    ) -> Field:
        """
        Creates and instantiates a new field and adds it to the record.
        """
        field = Field(
            id,
            self,
            label,
            datatype,
            primary_key=primary_key,
            foreign_keys=foreign_keys,
            description=description,
            options=options,
        )
        self._fields.append(field)
        return field

    @property
    def fields(self) -> Tuple[Field]:
        return tuple(self._fields)

    @property
    def primary_keys(self) -> Tuple[Field]:
        return tuple(f for f in self.fields if f.primary_key)

    def get_field(self, id: str) -> Field:
        for field in self.fields:
            if field.id == id:
                return field
        raise KeyError(f"Field '{id}' not found in record '{self.id}'")


class Schema(SchemaItem):
    """
    This is a common subclass for schema objects, whether tabular or hierarchical.
    """

    def __init__(
        self,
        id: str,
        description: Optional[str] = None,
        options: Optional[Mapping[str, Any]] = None,
    ):
        super().__init__(id, description, options)


class TabularSchema(Schema):
    """
    A tabular schema is a collection of datatypes and records. It is the equivalent of a database schema, Excel file
    with multiple sheets or a collection of CSV files.
    """

    def __init__(
        self,
        id: str,
        description: Optional[str] = None,
        version: str = None,
        datatypes: Iterable[Datatype] = STANDARD_TYPES,
        options: Optional[Mapping[str, Any]] = None,
    ):
        super().__init__(id, description, options)
        self._version = version
        self._records = []
        self._datatypes = tuple(datatypes or [])

    def add_record(
        self,
        id: str,
        label: str = None,
        description: Optional[str] = None,
        options: Optional[Mapping[str, Any]] = None,
    ) -> Record:
        """
        Creates and instantiates a new record and adds it to the schema.
        """
        if label is None:
            label = id

        record = Record(
            id,
            self,
            label=label,
            description=description,
            options=options,
        )
        self._records.append(record)
        return record

    @property
    def records(self) -> Tuple[Record]:
        return tuple(self._records)

    @property
    def datatypes(self) -> Tuple[Datatype]:
        return self._datatypes

    def get_record(self, id: str) -> Record:
        for record in self.records:
            if record.id == id:
                return record
        raise KeyError(f"Record '{id}' not found in schema '{self.id}'")

    def get_field(self, id: str) -> Field:
        if id.count(".") != 1:
            raise ValueError(
                f"Invalid field id '{id}'. Must be of format <record_id>.<field_id>"
            )
        record_id, field_id = id.split(".", 1)
        return self.get_record(record_id).get_field(field_id)

    def get_datatype(self, id: str) -> Datatype:
        if hasattr(id, "id"):
            id = id.id
        for datatype in self.datatypes:
            if datatype.id == id:
                return datatype
        raise KeyError(f"Datatype '{id}' not found in schema '{self.id}'")
