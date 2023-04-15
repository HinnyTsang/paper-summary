import time
from typing import Callable


def build_rate_limiter(rate_limit: int = 3) -> Callable[[], None]:
    """Sleep for 20 seconds to avoid rate limit (3 / minute)
    :param rate_limit: rate limit for the API call (requests / minute)
    :return: None
    """
    last_call_time = time.time()
    minimum_time = 60 / rate_limit

    def count_time() -> None:
        """Sleep for 20 seconds to avoid rate limit (3 / minute)"""
        nonlocal last_call_time
        while time.time() - last_call_time < minimum_time:
            sleep_time = minimum_time - (time.time() - last_call_time)
            time.sleep(sleep_time)
        last_call_time = time.time()
        return

    return count_time
