from starlette.requests import Request

from ..rabbitmq.call_rpc import call_rpc
from ..shared.exceptions.unauthorized_exception import UnauthorizedException


async def check_auth(request: Request):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if not access_token or not refresh_token:
        raise UnauthorizedException(detail="Unauthorized: missing tokens")

    result = await call_rpc(
        service_queue='auth_service_queue',
        message={'action': 'verify_token', 'token': access_token}
    )

    if not result or not result.get('valid') or not result.get('token_data'):
        raise UnauthorizedException(detail="Invalid token")

    return result
