import warnings
from typing import Dict, Optional

import falcon
from telegraf import TelegrafClient

from .base import Middleware
from .utils import merge_and_normalize


class LogHits(Middleware):

    def __init__(
            self,
            telegraf_client: Optional[TelegrafClient] = None,
            tags: Optional[Dict[str, str]] = None,
            metric_name_prefix: Optional[str] = None,
            metric_name: Optional[str] = None
    ) -> None:
        super().__init__(telegraf_client, tags, metric_name_prefix, metric_name)
        self._metric_name_prefix = self._metric_name_prefix or 'hits-'

    def process_response(self, req: falcon.Request, resp: falcon.Response, resource, req_succeeded: bool):
        tags = merge_and_normalize(
            self.get_tags(req, resp),
            req.context.get('telegraf_tags', {}),
            resp.context.get('telegraf_tags', {}),
        )
        values = merge_and_normalize(
                {
                    'hits': 1,
                },
                req.context.get('telegraf_values', {}),
                resp.context.get('telegraf_values', {}),
                cast=False,
            )
        self._telegraf.metric(
            self.get_metric_name(req),
            values=values,
            tags=tags,
        )


class LogHitsContextAware(LogHits):

    def __init__(
            self,
            telegraf_client: Optional[TelegrafClient] = None,
            tags: Optional[Dict[str, str]] = None,
            metric_name_prefix: Optional[str] = None,
            metric_name: Optional[str] = None
    ) -> None:
        super().__init__(telegraf_client, tags, metric_name_prefix, metric_name)
        warnings.warn('LogHitsContextAware middleware is deprecated.', DeprecationWarning)
