import falcon
import mockito
import pytest
import webtest
from telegraf import TelegrafClient

from falcon_telegraf import LogHits


@pytest.fixture
def telegraf_client():
    return mockito.mock(spec=TelegrafClient)


@pytest.fixture
def app(telegraf_client):
    api = falcon.API(
        middleware=[
            LogHits(telegraf_client=telegraf_client),
        ]
    )
    api.add_route('/x', AResource())
    api.add_route('/y/{id}', CResource())
    return api


@pytest.fixture
def webapi(app):
    return webtest.TestApp(app)


class AResource:

    def on_get(self, req, resp):
        resp.body = 'Success'


class CResource:
    def on_get(self, req, resp, id=None):
        req.context['telegraf_tags']['id'] = str(id)
        req.context['telegraf_values']['count'] = 5
        resp.context['telegraf_values']['foo'] = 'bar'
        resp.body = 'C rules'
