import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Class to define some settings of the database.
    Args:
        db_url: url o the database.
    """
    db_url: str = Field(..., env='DATABASE_URL')

settings = Settings()