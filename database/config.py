from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """ Instance stores all app settings, mainly environment variables """
    PROJECT_NAME: str = 'Recipe_for_You_backend'
    DB_PATH: Optional[str]

    class Config:
        env_prefix = 'RECIPE_BACKEND_'
        # uncomment when testing locally
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()
