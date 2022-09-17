from typing import Optional
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """ Instance stores all app settings, mainly environment variables """
    PROJECT_NAME: str = 'Recipe_for_You_backend'

    DB_PATH: Optional[str]

    class Config:
        env_prefix = 'RECIPE_BACKEND_'
        env_file = f'{BASE_DIR}/secrets/.env'
        env_file_encoding = 'utf-8'
        fields = {
            'DB_PATH': {'env': 'DB_PATH'}
        }


settings = Settings()
