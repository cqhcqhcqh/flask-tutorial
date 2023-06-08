import pytest
from flask import g, session
from flaskr.db import get_db

def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert response.headers['Location'] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None

# mark.parametrize decorator 这个 fixture 定义了 ('username', 'password', 'message') 三个参数
# 而且还一定义类一组测试数据，
# 这些测试数据最终会传递给 test_register_validate_input 函数
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered')
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    # response.data 是 bytes 
    # 所以要和 response.data 直接比较
    # message 也要是 bytes 类型
    # 所以上面的 message 都以`b` 开头，eg. b'Username is required.'
    # 如果不想比较 bytes 类型可以这么做
    # 'Username is required' in response.get_data(as_text=True)
    # `get_data` 返回的是一个 str 类型
    assert message in response.data

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == "/"

    # Using client in a with block allows accessing context variables
    # such as `session` after the response is returned

    # 因为 accessing session outside of a request would raise an error.
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()
    
    # client 就是之前定义的 @pytest.fixture def client(app) 函数所返回的 client 对象
    with client:
        auth.logout()
        assert 'user_id' not in session