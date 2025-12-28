from starlette.requests import Request
from starlette.responses import JSONResponse

from ....shared.default_response import default_content
from ....shared.errors.exceptions.bad_request_exception import BadRequestException


def register_bad_request_exception_handler(app):
    @app.exception_handler(BadRequestException)
    async def bad_request_handler(request: Request, exc: BadRequestException):
        return JSONResponse(
            status_code=400,
            content=default_content(has_error=True, message=exc.detail)
        )
