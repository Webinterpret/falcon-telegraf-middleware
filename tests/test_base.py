from unittest import mock

import falcon
from falcon import Request
from falcon import Response

from falcon_telegraf import LogHits


def test_base_methods():
    mwr = LogHits(
        telegraf_client=None,
        tags={'default': '1'},
    )
    req = request()
    resp = response()

    assert "hits-/v1/{id}/ping" == mwr.get_metric_name(req)
    assert {'default': '1', 'method': 'GET', 'status': '200 OK'} == mwr.get_tags(req, resp)


def test_metric_name_override():
    mwr = LogHits(
        telegraf_client=None,
        metric_name='my_metric'
    )
    req = request()

    assert "my_metric" == mwr.get_metric_name(req)


def test_metric_name_prefix():
    mwr = LogHits(
        telegraf_client=None,
        metric_name_prefix='abc:'
    )
    req = request()

    assert "abc:/v1/{id}/ping" == mwr.get_metric_name(req)


def request():
    req = mock.Mock(spec=Request)
    req.path = "/v1/1/ping"
    req.uri_template = "/v1/{id}/ping" 
    req.query_string = ''
    req.method = 'GET'
    return req

def response():
    resp = mock.Mock(spec=Response)
    resp.status = falcon.HTTP_200
    return resp
