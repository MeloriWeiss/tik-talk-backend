from starlette.requests import Request
from starlette.responses import JSONResponse

from ..default_response import default_content
from ..exceptions.unauthorized_exception import UnauthorizedException


def register_unauthorized_exception_handler(app):
    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(request: Request, exc: UnauthorizedException):
        return JSONResponse(
            status_code=401,
            content=default_content(has_error=True, message=exc.detail),
        )