import logging
from collections.abc import Awaitable, Callable

import uvicorn
from fastapi import FastAPI, Request, Response

from fullstack.config import ApplicationConfig

LOGGER = logging.getLogger(__name__)
REST_API_VERSION = "0.0.1"


async def add_api_version_header(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
):
    response = await call_next(request)
    response.headers["X-API-Version"] = REST_API_VERSION
    return response


def get_app(config: ApplicationConfig):
    app = FastAPI(version=REST_API_VERSION)
    app.middleware("http")(add_api_version_header)
    return app


def start(config: ApplicationConfig):
    app = get_app(config)

    assert config.rest.url.host is not None, "config.rest missing host"
    assert config.rest.url.port is not None, "config.rest missing port"
    uvicorn.run(app, host=config.rest.url.host, port=config.rest.url.port)
