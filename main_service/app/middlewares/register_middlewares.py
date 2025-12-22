from fastapi import FastAPI

from .logging.logging_middleware import register_logging_middleware


def register_middlewares(app: FastAPI):
    register_logging_middleware(app)