from typing import Dict, Optional
from warnings import warn

import falcon
from telegraf import TelegrafClient

RESERVED_TAGS = {'uri_template', 'method', 'status'}


class Middleware:
    def __init__(self,
                 telegraf_client: Optional[TelegrafClient] = None,
                 tags: Optional[Dict[str, str]] = None,
                 metric_name_prefix: Optional[str] = None,
                 metric_name: Optional[str] = None
                 ) -> None:
        self._telegraf = telegraf_client or TelegrafClient(host='localhost', port=8094)
        if all((metric_name_prefix, metric_name)):
            warn("Metric name prefix ignored - will use only metric_name={}".format(metric_name))
        self._metric_name_prefix = metric_name_prefix or ''
        self._metric_name = metric_name
        self._tags = tags or dict()
        if RESERVED_TAGS & set(self._tags.keys()):
            warn("Some default tags will be overwritten")

    def get_tags(self, req: falcon.Request, resp: falcon.Response) -> Dict[str, str]:
        tags = {}
        tags.update(self._tags)
        tags['method'] = req.method
        tags['status'] = resp.status[:3]
        tags['uri_template'] = req.uri_template
        return tags

    def get_metric_name(self, req: falcon.Request) -> str:
        if self._metric_name:
            return self._metric_name
        if not req.uri_template:
            # https://docs.influxdata.com/influxdb/v1.6/concepts/schema_and_data_layout/#discouraged-schema-design
            warn('URI template is available only while processing a response; going to use path')
        return self._metric_name_prefix + (req.uri_template or req.path)

    def process_request(self, req: falcon.Request, resp: falcon.Response):
        """Process the request before routing it.

        Args:
            req: Request object that will eventually be
                routed to an on_* responder method.
            resp: Response object that will be routed to
                the on_* responder.
        """
        req.context['telegraf_tags'] = {}
        req.context['telegraf_values'] = {}
        resp.context['telegraf_tags'] = {}
        resp.context['telegraf_values'] = {}

    def process_resource(self, req: falcon.Request, resp: falcon.Response, resource, params: Dict):
        """Process the request after routing.

        Note:
            This method is only called when the request matches
            a route to a resource.

        Args:
            req: Request object that will be passed to the
                routed responder.
            resp: Response object that will be passed to the
                responder.
            resource: Resource object to which the request was
                routed.
            params: A dict-like object representing any additional
                params derived from the route's URI template fields,
                that will be passed to the resource's responder
                method as keyword arguments.
        """

    def process_response(self, req: falcon.Request, resp: falcon.Response, resource, req_succeeded: bool):
        """Post-processing of the response (after routing).

        Args:
            req: Request object.
            resp: Response object.
            resource: Resource object to which the request was
                routed. May be None if no route was found
                for the request.
            req_succeeded: True if no exceptions were raised while
                the framework processed and routed the request;
                otherwise False.
        """
