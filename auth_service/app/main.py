from fastapi import FastAPI

from .rabbitmq.connection import lifespan
from .routers.tokens import tokens_router

app = FastAPI(lifespan=lifespan)
app.include_router(tokens_router)
