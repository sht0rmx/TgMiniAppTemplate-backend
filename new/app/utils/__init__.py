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


def create_hash(key: str | bytes, msg: str, from_env: bool = True, hex: bool = True) -> str | bytes:
    if isinstance(key, str):
        k = str(os.getenv(key)).encode() if from_env else key.encode()
    else:
        k = key

    h = hmac.new(k, msg.encode(), hashlib.sha256)
    return h.hexdigest() if hex else h.digest()