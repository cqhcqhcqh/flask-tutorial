import os 
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        # TESTING tells Flask that the app is in test mode.
        # Flask changes some internal behavior so it's easier to test,
        # and other extensions can also use the flag to make testing them
        # easier
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # After the test is over
    # the temporary file is closed and removed
    os.close(db_fd)
    os.unlink(db_path)

# client fixture
# Tests will use the client(create by `app.test_client()`) to make request
# to the application without running the server
@pytest.fixture
def client(app):
    return app.test_client()

# runner fixture
# creates a runner that can call the Click commands registered
# with the application
# Test will use the runner call the Click commands
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# The easiest way to do this in tests is to make a POST request to
# the login view with the client. Rather than writing that out every time

class AuthActions(object):
    # write a class with methods to do that,
    # and use a fixture（上面定义的 @pytest.fixture def client(app):) to pass it the client for each test
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )
    
    def logout(self):
        return self._client.get('/auth/logout')
    
@pytest.fixture
def auth(client):
    return AuthActions(client)