import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from modules.logger import logger
from modules.middleware import log_middleware
from modules.exceptions import http_exception_handler, validation_exception_handler

from api.main_page.router import router as router_home

from settings import (
    ConstSettings, 
    settings
)

class Application(FastAPI):
    """Setting up and preparing the launch of the application"""

    def __init__(self):
        self.logger = logger
        self.workflow = None
        self.directory = None

        super().__init__(
            title=ConstSettings.TITLE,
            debug=settings.APP_DEBUG,
            swagger_ui_parameters={
                "docExpansion": "none",
                "filter": "true",
                "operationsSorter": "method",
            },
            openapi_url="/openapi.yaml",
            lifespan=self.lifespan
        )
        self.run_startup_actions()

    def run_startup_actions(self):
        self.mount("/static", router_home)
        self.include_router(router=router_home)
        self.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
        self.add_exception_handler(HTTPException, http_exception_handler)
        self.add_exception_handler(RequestValidationError, validation_exception_handler)
        self.add_middleware(GZipMiddleware, minimum_size=1000)

app = Application()

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=9010, reload=True)
