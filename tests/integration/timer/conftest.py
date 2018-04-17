import time

import falcon
import mockito
import pytest
import webtest
from telegraf import TelegrafClient

from falcon_telegraf import Timer


@pytest.fixture
def telegraf_client():
    return mockito.mock(spec=TelegrafClient)


@pytest.fixture
def app(telegraf_client):
    api = falcon.API(
        middleware=[
            Timer(metric_name='timer', telegraf_client=telegraf_client),
        ]
    )
    api.add_route('/wait/{sec}', WaitResource())
    return api


@pytest.fixture
def webapi(app):
    return webtest.TestApp(app)


class WaitResource:
    def on_get(self, req, resp, sec=0.1):
        seconds = float(sec)
        time.sleep(seconds)
        resp.body = 'Have waited %1.1f seconds' % seconds
