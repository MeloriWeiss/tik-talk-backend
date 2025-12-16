from fastapi import FastAPI

from .routers.chats import chats_router

app = FastAPI()

app.include_router(chats_router)
