from fastapi import FastAPI

from .routers.accounts.accounts import accounts_router
from .routers.auth.auth import auth_router
from .routers.communities.communities import communities_router
from .routers.posts.posts import posts_router
from .shared.register_exception_handlers import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)

app.include_router(accounts_router)
app.include_router(posts_router)
app.include_router(auth_router)
app.include_router(communities_router)