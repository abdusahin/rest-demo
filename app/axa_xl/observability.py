import contextvars
import logging
import time
from typing import Any, Iterable

import bugsnag.handlers
from bugsnag.asgi import BugsnagMiddleware
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response

# configure session-id context
request_id_var = contextvars.ContextVar("request_id", default=None)
logger = logging.getLogger()


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_var.get()
        return True


def configure_request_id():
    for h in logger.handlers:
        h.addFilter(RequestIdFilter())


# setup bugnsag for error reporting
def configure_bugsnag(app: FastAPI):
    logger.info("Configure Bugsnag")
    app.add_middleware(BugsnagMiddleware)

    bugsnag_handler = bugsnag.handlers.BugsnagHandler()
    bugsnag_handler.setLevel(logging.ERROR)

    # get root logger and add the bugsnag handler
    root_logger = logging.getLogger()
    root_logger.addHandler(bugsnag_handler)


async def with_api_call_measurement(request: Request, callable) -> Response:
    start_time = time.perf_counter()
    response = await callable
    duration = time.perf_counter() - start_time
    logging.info("API timing", extra={"path": request.url.path, "method": request.method, "duration": duration})
    return response


async def with_database_call_measurement(query: str, query_params: Iterable[Any], callable) -> Response:
    start_time = time.perf_counter()
    response = await callable
    duration = time.perf_counter() - start_time
    logging.info("Database query timing", extra={"query": query, "query_params": query_params, "duration": duration})
    return response
