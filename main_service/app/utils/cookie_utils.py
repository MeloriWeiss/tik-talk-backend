from starlette.responses import Response

# ACCESS_TOKEN_LIFETIME = 900  # 15 минут
# REFRESH_TOKEN_LIFETIME = 604800  # 7 дней


def set_tokens_cookie(response: Response, tokens_dict: dict):
    access_token = tokens_dict.get("access_token")
    refresh_token = tokens_dict.get("refresh_token")

    if access_token:
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )

    if refresh_token:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )

def delete_tokens_cookie(response: Response):
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=0
    )
    response.set_cookie(
        key="refresh_token",
        value="",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=0
    )
