from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.adapters.in_.http.main import http_router
from src.core.application.jobs.assign_order_job import assign_order_job
from src.di.container import Container
from src.libs.errs.exceptions import DomainInvariantException, NotFoundException

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Delivery service started")

    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        assign_order_job,
        "interval",
        seconds=10,
    )
    scheduler.start()
    print("APScheduler started successfully.")
    yield
    scheduler.shutdown()
    print("APScheduler shut down successfully.")

    await Container.tear_down()

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
