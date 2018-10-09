from mockito import verify, any, contains


def test_middleware_called(webapi, telegraf_client):
    response = webapi.get('/a')
    assert response.text == 'Success'
    verify(telegraf_client, times=1).metric('hits-/a', values={'hits': 1}, tags={'path': '/a', 'method': 'GET'})


def test_middleware_called_n_times(webapi, telegraf_client):
    assert webapi.get('/a').text == 'Success'
    assert webapi.get('/a').text == 'Success'
    assert webapi.get('/a').text == 'Success'
    verify(telegraf_client, times=3).metric('hits-/a', values={'hits': 1}, tags={'path': '/a', 'method': 'GET'})


def test_middleware_called_mixed(webapi, telegraf_client):
    assert webapi.get('/a').status_code == 200
    assert webapi.get('/b').status_code == 200
    assert webapi.get('/c/1').status_code == 200
    verify(telegraf_client, times=3).metric(contains('hits-'), values={'hits': 1}, tags=any(dict))


def test_middleware_called_params(webapi, telegraf_client):
    assert webapi.get('/c/1?foo=1').status_code == 200
    verify(telegraf_client, times=1).metric('hits-/c/{id}',
                                            values={'hits': 1},
                                            tags={'path': '/c/1', 'query': 'foo=1', 'id': '1', 'method': 'GET'})
