from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from libs.errs.exceptions import DomainInvariantException, NotFoundException
from src.adapters.in_.http.main import router as http_router
from src.di.container import container

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Delivery service started")

    yield

    await container.tear_down()

    logger.info("Delivery service stopped")


app = FastAPI(
    title="Delivery Service",
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"code": "invalid_value", "message": str(exc)},
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    error_messages = [f"{e['loc'][-1]}: {e['msg']}" for e in errors]
    return JSONResponse(
        status_code=400,
        content={"code": "validation_error", "message": "; ".join(error_messages)},
    )


@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"code": exc.error.code, "message": exc.error.message},
    )


@app.exception_handler(DomainInvariantException)
async def domain_error_handler(request: Request, exc: DomainInvariantException) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"code": exc.error.code, "message": exc.error.message},
    )


@app.exception_handler(Exception)
async def global_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception")
    return JSONResponse(status_code=500, content=None)


app.include_router(http_router)
