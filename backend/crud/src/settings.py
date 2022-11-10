import os
from functools import lru_cache

from pydantic import BaseSettings, Field


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_DIR = os.path.join(ROOT_DIR, 'default')


class Settings(BaseSettings):
    app_name: str = "CRUD Project"
    db_path: str = Field(env='DATABASE_URL', default='sqlite://db.sqlite3')

    class Config:
        env_file = ".prod.env"


@lru_cache()
def get_settings():
    return Settings()
