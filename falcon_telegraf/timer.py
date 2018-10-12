from typing import Dict, Optional

import falcon
from telegraf import TelegrafClient

from .base import Middleware
from .utils import merge_and_normalize_tags

START_TIME = 'x-start-time'


def timer():
    """Multiplying is done to return millis and keep backwards compatibility.
    """
    try:
        from time import perf_counter
        return int(round(perf_counter() * 1000))
    except ImportError:
        from time import time
        return int(round(time() * 1000))


class Timer(Middleware):
    def __init__(
            self,
            telegraf_client: Optional[TelegrafClient] = None,
            tags: Optional[Dict[str, str]] = None,
            metric_name_prefix: Optional[str] = None,
            metric_name: Optional[str] = None
    ) -> None:
        super().__init__(telegraf_client, tags, metric_name_prefix, metric_name)
        self._metric_name_prefix = self._metric_name_prefix or 'time-'

    def process_request(self, req: falcon.Request, resp: falcon.Response):
        req.context[START_TIME] = timer()

    def process_response(self, req: falcon.Request, resp: falcon.Response, resource, req_succeeded: bool):
        try:
            delta = timer() - req.context.pop(START_TIME)
            tags = merge_and_normalize_tags(self.get_tags(req, resp), req.context, resp.context)
            self._telegraf.metric(
                self.get_metric_name(req),
                values={
                    'hits': 1,
                    'time_delta': delta,
                },
                tags=tags,
            )
        except KeyError:
            pass  # unprocessed by this MWare
