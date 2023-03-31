import datetime
import decimal
from typing import Optional


def _try_parse_time(time: str, format: str) -> Optional[datetime.time]:
    try:
        return datetime.datetime.strptime(time, format).time()
    except ValueError:
        return None


def try_normalize_timestring(date: datetime.date, s: str) -> Optional[int]:
    """Attempts to normalize time string into unix timestamp in microseconds."""
    time = _try_parse_time(s, '%H:%M:%S') or _try_parse_time(s, '%H:%M')
    if time is None:
        return None
    dt = datetime.datetime.combine(date, time, tzinfo=datetime.timezone.utc)
    return int(dt.timestamp() * 1000 * 1000)


def try_normalize_timestamp(timestamp: decimal.Decimal) -> Optional[int]:
    """Attempts to normalize timestamp into unix timestamp in microseconds."""
    if timestamp < 10 ** 8:
        return None
    elif timestamp < 10 ** 10:
        return int(timestamp * 1000 * 1000)
    elif timestamp < 10 ** 13:
        return int(timestamp * 1000)
    elif timestamp < 10 ** 16:
        return int(timestamp)
    else:
        return None
