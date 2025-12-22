from starlette.requests import Request
from starlette.responses import JSONResponse

from ....shared.default_response import default_content
from ....shared.errors.exceptions.not_found_exception import NotFoundException


def register_not_found_exception_handler(app):
    @app.exception_handler(NotFoundException)
    async def not_found_handler(request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=404,
            content=default_content(has_error=True, message=exc.detail)
        )
