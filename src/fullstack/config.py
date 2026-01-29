from typing import Literal

from pydantic import BaseModel, ConfigDict, HttpUrl


class Config(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_default=True,
    )


LogLevel = Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class RestConfig(Config):
    url: HttpUrl = HttpUrl("http://localhost:8000")


class LoggingConfig(Config):
    level: LogLevel = "INFO"


class DatabaseConfig(Config):
    initialise: bool = True


class SQLiteConfig(DatabaseConfig):
    file_name: str = "database.db"


class ApplicationConfig(Config):
    rest: RestConfig = RestConfig()
    logging: LoggingConfig = LoggingConfig()
    database: DatabaseConfig = SQLiteConfig()
