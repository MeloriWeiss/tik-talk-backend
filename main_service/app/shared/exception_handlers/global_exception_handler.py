from starlette.requests import Request
from starlette.responses import JSONResponse

from ..default_response import default_content
from ..exceptions.bad_request_exception import BadRequestException


def register_global_exception_handler(app):
    @app.exception_handler(Exception)
    async def global_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=default_content(has_error=True, message="Internal server error")
        )
