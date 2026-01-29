from collections.abc import AsyncGenerator
from functools import cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

from fullstack.config import DatabaseConfig, SQLiteConfig

_engine: Engine | None = None


@cache
def get_engine() -> Engine:
    if _engine is None:
        raise ValueError("Database configuration incomplete!")
    return _engine


def configure_engine(config: DatabaseConfig):
    if isinstance(config, SQLiteConfig):
        global _engine
        _engine = create_engine(
            f"sqlite:///{config.file_name}",
            echo=True,
            connect_args={"check_same_thread": False},
        )
    else:
        raise ValueError(f"Unknown DatabaseConfig type: {type(config)}")


async def get_session() -> AsyncGenerator[Session]:
    with Session(get_engine()) as session:
        yield session


def setup_database(config: DatabaseConfig):
    configure_engine(config)
    if config.initialise:
        SQLModel.metadata.create_all(get_engine())


SessionDep = Annotated[Session, Depends(get_session)]
