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
    api.add_route('/a', AResource())
    api.add_route('/b', BResource())
    api.add_route('/c/{id}', CResource())
    return api


@pytest.fixture
def webapi(app):
    return webtest.TestApp(app)


class AResource:

    def on_get(self, req, resp):
        resp.text = 'Success'


class BResource:
    def on_get(self, req, resp):
        req.context['telegraf_tags']['adventure'] = 'time'
        resp.text = 'Algebraic!'


class CResource:
    def on_get(self, req, resp, id=None):
        req.context['telegraf_tags']['id'] = str(id)
        resp.text = 'C rules'
