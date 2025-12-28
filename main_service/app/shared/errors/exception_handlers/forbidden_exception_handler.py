from starlette.requests import Request
from starlette.responses import JSONResponse

from ..exceptions.forbidden_exception import ForbiddenException
from ....shared.default_response import default_content
from ....shared.errors.exceptions.bad_request_exception import BadRequestException


def register_forbidden_exception_handler(app):
    @app.exception_handler(ForbiddenException)
    async def forbidden_handler(request: Request, exc: ForbiddenException):
        return JSONResponse(
            status_code=403,
            content=default_content(has_error=True, message=exc.detail)
        )
