from typing import Callable
from libs.exceptions import RequestError


def retry(max_retries: int = 3) -> Callable:
    def decorator_retry(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs) -> Callable:
            current_tries = 0
            response, message_error = None, ''
            while current_tries < max_retries and response is None:
                current_tries += 1
                response, error_message = await func(*args, **kwargs)
            if response is None:
                raise RequestError(error_message)
            return response
        return wrapper

    return decorator_retry