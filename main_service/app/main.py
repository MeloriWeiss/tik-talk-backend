from fastapi import FastAPI

from .middlewares.register_middlewares import register_middlewares
from .routers.accounts.accounts import accounts_router
from .routers.auth.auth import auth_router
from .routers.chats.chats import chats_router
from .routers.communities.communities import communities_router
from .routers.messages.messages import messages_router
from .routers.posts.posts import posts_router
from .shared.errors.register_exception_handlers import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)
register_middlewares(app)

app.include_router(accounts_router)
app.include_router(posts_router)
app.include_router(auth_router)
app.include_router(communities_router)
app.include_router(chats_router)
app.include_router(messages_router)