import datetime
from typing import Any
from pydantic import BaseModel

from app.config.model import BaseConfig

def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )

class BaseDomainModel(BaseModel):
    Config = BaseConfig
    Config.from_attributes = True
    Config.validate_assignment = True
    Config.allow_population_by_field_name = True
    Config.json_encoders = {datetime.datetime: convert_datetime_to_realworld}
    Config.alias_generator = convert_field_to_camel_case