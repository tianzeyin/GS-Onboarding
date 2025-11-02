from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException
from loguru import logger
from time import perf_counter

class LoggerMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        start_time = perf_counter()      
        logger.info(f"{request.method} {request.url.path}")

        try:
            response: Response = await call_next(request)

            process_time = (perf_counter() - start_time) * 1000
            logger.info(
                f"{request.method} {request.url.path} "
                f"{response.status_code} in {process_time:.2f}ms"
            )

            return response
        except Exception as e:
            # Log unexpected errors
            process_time = (perf_counter() - start_time) * 1000
            logger.error(
                f"{request.method} {request.url.path} "
                f"ERROR in {process_time:.2f}ms: {str(e)}"
            )
            raise