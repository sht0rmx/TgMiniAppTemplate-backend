from datetime import datetime, timedelta, timezone
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