from functools import lru_cache
from typing import List

from pydantic import PostgresDsn

class AppSettings() :
    allowed_host : List[str] = ["*"]
    database_url : PostgresDsn

    min_connection_count : int = 10
    max_connection_count : int = 20

@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()