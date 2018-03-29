from typing import Dict, Optional

import falcon
from telegraf import TelegrafClient

from falcon_telegraf.base import Middleware


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

    def process_resource(self, req: falcon.Request, resp: falcon.Response, resource, params: Dict):
        self.metric(req)

    def metric(self, req):
        self._telegraf.metric(
            self.get_metric_name(req),
            values={
                'hits': 1,
            },
            tags=self.get_tags(req),
        )


class LogHitsContextAware(LogHits):
    def process_resource(self, req: falcon.Request, resp: falcon.Response, resource, params: Dict):
        pass

    def process_response(self, req: falcon.Request, resp: falcon.Response, resource, req_succeeded: bool):
        self.metric(req)

    def get_tags(self, req: falcon.Request) -> Dict[str, str]:
        tags = super().get_tags(req)
        for k, v in req.context.items():
            tags[str(k)] = str(v)
        return tags
