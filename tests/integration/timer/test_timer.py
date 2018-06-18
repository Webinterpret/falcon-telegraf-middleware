from mockito import when, captor, any_


def test_middleware_called(webapi, telegraf_client):
    values_captor = captor(any_(dict))
    when(telegraf_client).metric(
        'timer',
        values=values_captor,
        tags={'path': '/wait/0.2', 'success': 'True'}
    )
    response = webapi.get('/wait/0.2')
    assert response.text == 'Have waited 0.2 seconds'
    assert int(values_captor.value['time_delta'] / 100) == 2
