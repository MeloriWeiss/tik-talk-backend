from ...database import async_session
from ...models.models import HttpLog


async def save_log(data: dict):
    async with async_session() as session:
        log = HttpLog(
            timestamp=data.get('timestamp'),
            level=data.get('level'),
            service=data.get('service'),
            request_id=data.get('request_id'),
            method=data.get('method'),
            path=data.get('path'),
            status_code=data.get('status_code'),
            duration_ms=data.get('duration_ms'),
            client_ip=data.get('client_ip'),
            message=data.get('message'),
        )

        session.add(log)
        await session.commit()
