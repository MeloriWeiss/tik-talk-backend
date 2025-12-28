from datetime import datetime


def serialize_datetime(data: dict):
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    serialize_datetime(item)
        elif isinstance(value, dict):
            serialize_datetime(value)
    return data