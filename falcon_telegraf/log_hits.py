from typing import Dict

import falcon
from telegraf import TelegrafClient

from falcon_telegraf.base import Middleware


class LogHits(Middleware):

    def __init__(self,
                 telegraf_client: TelegrafClient,
                 tags: Dict[str, str] = None,
                 metric_name_prefix: str = None
                 ) -> None:
        super().__init__()
        self._telegraf = telegraf_client
        self._metric_name_prefix = metric_name_prefix
        self._tags = tags

    def process_request(self, req: falcon.Request, resp: falcon.Response):
        self._telegraf.metric(
            self.get_metric_name(req),
            values={
                'request': 1,
            },
            tags=self.get_tags(req),
        )

    def get_tags(self, req):
        tags = {}
        tags.update(self._tags)
        tags['path'] = req.relative_uri
        return tags

    def get_metric_name(self, req: falcon.Request):
        return self._metric_name_prefix + req.relative_uri
