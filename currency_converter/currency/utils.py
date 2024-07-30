"""Decorators."""
import time
import logging
from typing import Callable, Tuple, Dict

from requests import Response

logger = logging.getLogger(__name__)


def reconnect_decorator(retries: int = 3, delay: int = 3) -> Callable:
    def decorator(func: Callable) -> Callable:
        """Decorate a function."""
        def wrapper(*args: Tuple, **kwargs: Dict) -> Response:
            """Wrapper a function."""
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    logger.warning(f'Ошибка №{attempt} при получении курса валют: {error}')
                    time.sleep(delay)
            raise ConnectionError()
        return wrapper
    return decorator
