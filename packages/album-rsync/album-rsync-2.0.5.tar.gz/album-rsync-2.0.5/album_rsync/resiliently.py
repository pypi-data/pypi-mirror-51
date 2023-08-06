import logging
import backoff
from .throttle import Throttle

class Resiliently:
    def __init__(self, config):
        self._config = config
        self._throttler = Throttle()
        if config.verbose:
            logging.getLogger('backoff').addHandler(logging.StreamHandler())

    def call(self, func, *args, **kwargs):
        return self._throttle(self._retry, func, *args, **kwargs)

    def _throttle(self, func, *args, **kwargs):
        return self._throttler.throttle(delay_sec=self._config.throttling)(func)(*args, **kwargs)

    def _retry(self, func, *args, **kwargs):
        # We +1 this because backoff retries UP to and not including max_retries
        max_tries = self._config.retry + 1
        return backoff.on_exception(backoff.expo, Exception, max_tries=max_tries)(func)(*args, **kwargs)
