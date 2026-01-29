import logging
from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, Response

from fullstack.config import ApplicationConfig
from fullstack.db import setup_database

from .applicant import applicant_router
from .application import application_router
from .exercise import exercise_router
from .reporting import reporting_router

LOGGER = logging.getLogger(__name__)
REST_API_VERSION = "0.0.1"


def lifespan(config: ApplicationConfig):
    @asynccontextmanager
    async def inner(app: FastAPI):
        setup_database(config.database)
        yield

    return inner


async def add_api_version_header(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
):
    response = await call_next(request)
    response.headers["X-API-Version"] = REST_API_VERSION
    return response


def get_app(config: ApplicationConfig):
    app = FastAPI(version=REST_API_VERSION, lifespan=lifespan(config))
    app.middleware("http")(add_api_version_header)
    app.include_router(applicant_router)
    app.include_router(exercise_router)
    app.include_router(application_router)
    app.include_router(reporting_router)
    return app


def start(config: ApplicationConfig):
    app = get_app(config)

    assert config.rest.url.host is not None, "config.rest missing host"
    assert config.rest.url.port is not None, "config.rest missing port"
    uvicorn.run(app, host=config.rest.url.host, port=config.rest.url.port)
