import json
import logging
import time
import uuid

from fastapi import FastAPI
from starlette.requests import Request

from ...utils.send_log import send_log

# logger = logging.getLogger("main_service_logger")
# logger.setLevel(logging.INFO)
#
# class JsonFormatter(logging.Formatter):
#     def format(self, record):
#         log_record = {
#             "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
#             "level": record.levelname,
#             "service": "fastapi_app",
#             "message": record.getMessage()
#         }
#         return json.dumps(log_record)

# handler = logging.FileHandler('/app/logs/app.log')
# handler.setFormatter(JsonFormatter())
# logger.addHandler(handler)

def register_logging_middleware(app: FastAPI):
    @app.middleware("logging")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = int((time.time() - start_time) * 1000)

        status_code = response.status_code
        log_level = "info"

        if status_code >= 500:
            log_level = "critical"
        elif status_code >= 400:
            log_level = "error"
        else:
            log_level = "info"

        log_data = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "level": log_level,
            "service": "main_service",
            "request_id": request.headers.get("X-Request-ID") or str(uuid.uuid4()),
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration,
            "client_ip": request.client.host,
            "message": "Request processed"
        }
        log_json = json.dumps(log_data)
        # log_json = json.dumps({"log_data": "log_data"})
        # logger.info(log_json)

        await send_log(log_json, log_level)

        return response
