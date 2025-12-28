from fastapi import FastAPI

from .rabbitmq.connection import lifespan
from .routers.http_logs.http_logs import http_logs_router
from .shared.errors.register_exception_handlers import register_exception_handlers

app = FastAPI(lifespan=lifespan, root_path='/logs')

register_exception_handlers(app)

app.include_router(http_logs_router)
