"""
This library provides additional functionality for HTTP requests.
"""

# Import from standard libraries
from functools import wraps, partial
import logging
from time import sleep
from typing import Callable

# Import from third-party libraries
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout


def retry(
    func: Callable = None,
    max_retry: int = 5,
    wait_time: float = 0.5,
    retry_exponent: float = 1.1,
    no_retry_codes: list[int] = None,
    connection_error_wait: int = 2
):
    """
    A decorator that handles retries for HTTP requests.
    :param func: the function to be decorated
    :param max_retry: maximum number of retries to be done.
    :param wait_time: base wait time, which will be multiplied.
    :param retry_exponent: multiplier to exponentiate in exponential backoff
    :param retry_codes: the default list of status codes that are retried.
        By default, these are: [429, 502, 503, 504].
    :param connection_error_wait: how long the retry waits in the event of a connection error.
    """
    if func is None:
        return partial(
            retry,
            max_retry=5,
            wait_time=0.5,
            retry_exponent=1.1,
            retry_codes=None,
            connection_error_wait=2,
        )

    if no_retry_codes is None:
        no_retry_codes = [400, 401, 403, 404]

    @wraps(func)
    def inner(*args, **kwargs):
        retries = 0
        while retries <= max_retry:
            try:
                return func(*args, **kwargs)
            except (ConnectionError, Timeout):
                print("Connection error, please check your internet connection.")
                print("API call will retry until non-connection errors are encountered.")
                sleep(connection_error_wait)
            except (RequestException, HTTPError) as error:
                error_code = error.response.status_code
                msg = (f'An error occurred with error code {error_code}.\n '
                       f'Error Message: {error.response.text}')
                logging.error(msg)
                logging.exception(error)
                print(msg)
                if error_code not in no_retry_codes and retries < max_retry:
                    msg = f"Status code {error_code} OK to be retried, retrying."
                    logging.error(msg)
                    print(msg)
                    sleep(wait_time * (retry_exponent ** retries))
                    retries += 1
                elif error_code not in no_retry_codes and retries == max_retry:
                    msg = "Reached maximum retries, raising."
                    logging.error(msg)
                    print(msg)
                    raise
                else:
                    msg = "Error code within no-retry list. Raising."
                    print(msg)
                    logging.error(msg)
                    raise
    return inner
