from datetime import datetime, timedelta
import hashlib
import hmac
import os
import re


def parse_expire(date: str) -> timedelta:
    match = re.match(r"(\d+)([smhd])", date)
    if not match:
        raise ValueError(f"Invalid expire format: {date}")
    val, unit = match.groups()
    val = int(val)
    if unit == "s":
        return timedelta(seconds=val)
    elif unit == "m":
        return timedelta(minutes=val)
    elif unit == "h":
        return timedelta(hours=val)
    elif unit == "d":
        return timedelta(days=val)
    else:
        raise ValueError(f"Unknown unit: {unit}")


def is_date_expired(created, expire_delta: str) -> bool:    
    return datetime.now() > (created + parse_expire(expire_delta))


def create_hash(key:str, msg:str, from_env:bool=True) -> str:
    return hmac.new(key=str(os.getenv(key) if from_env else key).encode("utf-8"),
                            msg=msg.encode("utf-8"),
                            digestmod=hashlib.sha256).hexdigest()