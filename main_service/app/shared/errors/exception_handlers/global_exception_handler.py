from starlette.requests import Request
from starlette.responses import JSONResponse

from ....shared.default_response import default_content


def register_global_exception_handler(app):
    @app.exception_handler(Exception)
    async def global_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=400,
            content=default_content(has_error=True, message="Bad request")
        )
