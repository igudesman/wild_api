import datetime

from typing import Callable
from libs.exceptions import RequestError


def retry(max_retries: int = 3) -> Callable:
    def decorator_retry(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs) -> Callable:
            current_tries = 0
            response, error_message = None, ''
            while current_tries < max_retries and response is None:
                current_tries += 1
                response, error_message = await func(*args, **kwargs)
            if response is None:
                raise RequestError(error_message)
            return response
        return wrapper

    return decorator_retry


def get_current_week_range(date=None) -> str:
    if date is None:
        date = datetime.date.today()
    _, _, day_of_week = date.isocalendar()
    week_from_day = date - datetime.timedelta(days=day_of_week - 1)
    for i in range(7):
        yield (week_from_day + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
