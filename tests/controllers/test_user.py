from tests.utils import request
from app.utils.messages.message import USERNAME_DUPLICATED, INVALID_CREDENTIALS


class TestRegister:
    def test_register_valid(self, client):
        data = {
            'username': 'test@name',
            'password': 'Abc@.12345'
        }
        rv = request.post(client, '/register', data)
        assert rv.status_code == 200

    def test_register_duplicate_username(self, client):
        data = {
            'username': 'tung',
            'password': '654321'
        }
        rv = request.post(client, '/register', data)
        assert rv.status_code == 409
        assert rv.get_json()['message'] == USERNAME_DUPLICATED

    def test_register_invalid_password(self, client):
        data = {
            'username': 'new_user',
            'password': '654  321'
        }
        rv = request.post(client, '/register', data)
        assert rv.status_code == 400

    def test_register_invalid_field_type(self, client):
        data = {
            'username': 'new_user',
            'password': 654321
        }
        rv = request.post(client, '/register', data)
        assert rv.status_code == 400

    def test_register_missing_field(self, client):
        data = {
            'username': 'new_user'
        }
        rv = request.post(client, '/register', data)
        assert rv.status_code == 400

    def test_register_invalid_field_length(self, client):
        data = {
            'username': 'u' * 100,
            'password': '1232144'
        }
        rv = request.post(client, '/register', data)
        assert rv.status_code == 400


class TestLogin:
    def test_login_valid(self, client):
        data = {
            'username': 'tung',
            'password': '123456'
        }
        rv = request.post(client, '/login', data)
        assert rv.status_code == 200
        assert rv.get_json()['access_token']

    def test_login_wrong_password(self, client):
        data = {
            'username': 'tung',
            'password': '111111'
        }
        rv = request.post(client, '/login', data)
        assert rv.status_code == 401
        assert rv.get_json()['message'] == INVALID_CREDENTIALS

    def test_login_wrong_username(self, client):
        data = {
            'username': 'wrong',
            'password': '111111'
        }
        rv = request.post(client, '/login', data)
        assert rv.status_code == 401
        assert rv.get_json()['message'] == INVALID_CREDENTIALS

    def test_login_missing_field(self, client):
        data = {
            'username': 'tung'
        }
        rv = request.post(client, '/login', data)
        assert rv.status_code == 400

    def test_login_invalid_field_type(self, client):
        data = {
            'username': 'tung',
            'password': 123456
        }
        rv = request.post(client, '/login', data)
        assert rv.status_code == 400

    def test_login_unknown_field(self, client):
        data = {
            'username': 'tung',
            'password': '123456',
            'valid': True
        }
        rv = request.post(client, '/login', data)
        assert rv.status_code == 400
