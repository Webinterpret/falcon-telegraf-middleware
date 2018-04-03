from unittest import mock

import mockito
from falcon import Request, Response
from telegraf import TelegrafClient

from falcon_telegraf import LogHits
from falcon_telegraf import LogHitsContextAware


def test_log_hits():
    tc = mockito.mock(spec=TelegrafClient, strict=True)
    mockito.when(tc).metric(
        'hits-/v1/ping',
        values={
            'hits': 1,
        },
        tags={'path': '/v1/ping'},
    )
    mwr = LogHits(
        telegraf_client=tc,
    )
    req = request()
    req.context = {'foo': 'bar'}
    mwr.process_resource(req, response(), None, None)


def test_log_hits_with_context():
    tc = mockito.mock(spec=TelegrafClient, strict=True)
    mockito.when(tc).metric(
        'hits-/v1/ping',
        values={
            'hits': 1,
        },
        tags={'path': '/v1/ping',
              'foo': 'bar',
              'success': 'True'},
    )
    mwr = LogHitsContextAware(
        telegraf_client=tc,
    )
    req = request()
    req.context = {'foo': 'bar'}
    mwr.process_response(req, response(), None, True)


def request():
    req = mock.Mock(spec=Request)
    req.path = "/v1/ping"
    req.query_string = ''
    return req


def response():
    resp = mock.Mock(spec=Response)
    resp.context = {}
    return resp
