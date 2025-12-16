from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..default_response import default_content


def register_http_default_exception_handler(app):
    @app.exception_handler(HTTPException)
    async def http_default_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=400,
            content=default_content(has_error=True, message=exc.detail)
        )
