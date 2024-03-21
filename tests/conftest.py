from pathlib import Path

import pytest

from sfdata_schema.spec import TabularSchema


@pytest.fixture
def base_dir():
    base_dir = Path(__file__).parent.parent
    assert (base_dir / "pyproject.toml").exists()
    return base_dir


@pytest.fixture
def dist_dir(base_dir):
    dist_dir = base_dir / "dist"
    dist_dir.mkdir(exist_ok=True)
    return dist_dir


@pytest.fixture
def pet_schema():
    schema = TabularSchema(id="person_schema")
    person_record = schema.add_record("person", options={"color": "LightPink"})
    person_record.add_field("id", primary_key=True)
    person_record.add_field("first_name")
    person_record.add_field("last_name")

    pet_record = schema.add_record("pet")
    pet_record.add_field("id", primary_key=True)
    pet_record.add_field("owner_id", foreign_keys=["person.id"])
    pet_record.add_field("name")

    address_record = schema.add_record("address")
    address_record.add_field("owner_id", primary_key=True, foreign_keys=["person.id"])
    address_record.add_field("type", primary_key=True)
    address_record.add_field("address")

    primary_phone_record = schema.add_record("primary_phone")
    primary_phone_record.add_field("id", primary_key=True, foreign_keys=["person.id"])
    primary_phone_record.add_field("number")

    return schema
