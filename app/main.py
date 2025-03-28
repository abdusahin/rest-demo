import asyncio
import logging
import time
import uuid
from asyncio import exceptions
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from starlette.responses import JSONResponse

from app.axa_xl import endpoints
from app.axa_xl.config import load_environment_variables
from app.axa_xl.database.db_operations import ConnectionProvider
from app.axa_xl.observability import request_id_var, configure_request_id, configure_bugsnag, with_api_call_measurement

logger = logging.getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create DB connection provider
    await ConnectionProvider.create()
    yield


app = FastAPI(title="demo", version="0.1.0", lifespan=lifespan)
REQUEST_TIMEOUT_SECS = 15

app.include_router(endpoints.router, prefix="/api", tags=["API"])

load_environment_variables()
configure_request_id()
configure_bugsnag(app)


@app.get("/", include_in_schema=False)
def root():
    """
    Redirects root URL to API documentation.
    """
    return RedirectResponse(url="/docs")


@app.middleware("http")
async def configure_request(request: Request, call_next):
    request_uuid = str(uuid.uuid4())
    request_id = request_uuid.split('-')[-1]
    request_id_var.set(request_id)
    try:
        coro = asyncio.wait_for(call_next(request), timeout=REQUEST_TIMEOUT_SECS)
        response = await with_api_call_measurement(request, coro)
        response.headers['request-id'] = request_id
        return response
    except exceptions.TimeoutError:
        logger.error("Timeout error")
        return JSONResponse(
            status_code=503,
            headers={'request-id': request_id},
            content={"detail": {
                "message": "Server failed to process the request on time"
            }})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled error", extra={"exception": str(exc)})
    return JSONResponse(
        status_code=503,
        content={"detail": {
            "message": f"Unhandled server error {str(exc)}"
        }},
    )
