from unittest import mock

import mockito
from falcon import Request, Response
from telegraf import TelegrafClient

from falcon_telegraf import LogHits


def test_log_hits():
    tc = mockito.mock(spec=TelegrafClient, strict=True)
    mockito.when(tc).metric(
        'hits-/v1/{id}/ping',
        values={
            'hits': 1,
        },
        tags={
            'path': '/v1/1/ping',
            'foo': 'bar',
            'method': 'GET',
            'success': 'True',
        },
    )
    mwr = LogHits(
        telegraf_client=tc,
    )
    req = request()
    req.context = {'foo': 'bar'}
    mwr.process_resource(req, response(), None, True)


def request():
    req = mock.Mock(spec=Request)
    req.path = "/v1/1/ping"
    req.uri_template = "/v1/{id}/ping"
    req.query_string = ''
    req.method = 'GET'
    return req


def response():
    resp = mock.Mock(spec=Response)
    resp.context = {}
    return resp
