from flaskr import create_app

def test_config():
    # The only behavior that can change is passing test config or not
    assert not create_app().testing
    assert create_app({ 'TESTING': True }).testing

def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'hello, world!'