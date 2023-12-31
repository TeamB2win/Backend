import os
from distutils.util import strtobool
from functools import lru_cache
from typing import List

from pydantic import PostgresDsn

class AppSettings() :
    allowed_hosts : List[str] = ["*"]
    database_url : PostgresDsn

    min_connection_count : int = 10
    max_connection_count : int = 20
    docs_url : str = "/docs" if strtobool(os.environ["DOCS_ENABLE"]) else None
    redoc_url : str = "/redoc" if strtobool(os.environ["DOCS_ENABLE"]) else None
    
    postgres_user: str = "postgres"
    postgres_password: str = "1234"
    postgres_server: str = "172.17.0.1"
    postgres_port: str = "5432"
    postgres_db: str = "b2win"
    db_echo_log: bool = True
    
    @property
    def sync_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
    

@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()