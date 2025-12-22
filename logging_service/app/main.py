from fastapi import FastAPI

from .rabbitmq.connection import lifespan

app = FastAPI(lifespan=lifespan)
