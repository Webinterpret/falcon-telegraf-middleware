import falcon
import mockito
import pytest
import webtest
from telegraf import TelegrafClient

from falcon_telegraf import LogHits
from falcon_telegraf import LogHitsContextAware


@pytest.fixture
def telegraf_client():
    return mockito.mock(spec=TelegrafClient)


@pytest.fixture
def app(telegraf_client):
    api = falcon.API(
        middleware=[
            LogHits(telegraf_client=telegraf_client),
            LogHitsContextAware(telegraf_client=telegraf_client),
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
        req.context['id'] = str(id)
        resp.body = 'C rules'
