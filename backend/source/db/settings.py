from pydantic import BaseModel
import os


class DatabaseSettings(BaseModel):
    user: str
    password: str
    host: str
    port: str
    db_name: str


def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings(
        user=os.getenv("DB_USER", 'postgres'),
        password=os.getenv("DB_PASSWORD", '123'),
        host=os.getenv("DB_HOST", 'localhost'),
        port=os.getenv("DB_PORT", '5432'),
        db_name=os.getenv("DB_NAME", 'tms'),
    )

