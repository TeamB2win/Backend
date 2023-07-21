
from typing import Any
from pydantic import ConfigDict

class BaseConfig(ConfigDict):
    from_attributes: bool
    validate_assignment: bool
    allow_population_by_field_name: bool
    json_encoders: dict
    alias_generator: Any