from mockito import verify, any_


def test_middleware_called_no_params(webapi, telegraf_client):
    response = webapi.get('/x')
    assert response.text == 'Success'
    verify(telegraf_client, times=1).metric('hits-/x', values={'hits': 1}, tags={'path': '/x', 'method': 'GET'})


def test_middleware_called_params(webapi, telegraf_client):
    assert webapi.get('/y/1?foo=1').status_code == 200
    verify(telegraf_client, times=2).metric(
        'hits-/y/{id}',
        values={'hits': 1},
        tags=any_(dict),
    )
