from unittest import mock

from falcon import Request

from falcon_telegraf import LogHits


def test_base_methods():
    mwr = LogHits(
        telegraf_client=None,
        tags={'default': '1'},
    )
    req = request()

    assert "hits-/v1/ping" == mwr.get_metric_name(req)
    assert {'default': '1', 'path': '/v1/ping'} == mwr.get_tags(req)


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

    assert "abc:/v1/ping" == mwr.get_metric_name(req)


def request():
    req = mock.Mock(spec=Request)
    req.path = "/v1/ping"
    req.query_string = ''
    return req
