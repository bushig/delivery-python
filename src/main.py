from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from adapters.out.postgres.database import engine
from libs.errs.exceptions import DomainInvariantException, NotFoundException

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Delivery service started")

    yield

    await engine.dispose()

    logger.info("Delivery service stopped")


app = FastAPI(
    title="Delivery Service",
    version="1.0.0",
    lifespan=lifespan,
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
