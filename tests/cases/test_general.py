from tests.utils import request
from app.utils.messages.message import INVALID_TOKEN, MISSING_TOKEN


def post_request(client, access_token):
    data = {
        'name': 'test_cat',
        'description': 'testing'
    }
    return request.post(client, '/categories', data, access_token)


class TestToken:
    def test_missing_token(self, client):
        rv = post_request(client, '')
        assert rv.get_json()['message'] == MISSING_TOKEN

    def test_invalid_token(self, client):
        rv = post_request(client, 'Bearer')
        assert rv.get_json()['message'] == INVALID_TOKEN
        rv = post_request(client,
                          'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                          'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.'
                          'SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c')
        assert rv.get_json()['message'] == INVALID_TOKEN
        rv = post_request(client, 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                                  'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.'
                                  'SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c')
        assert rv.get_json()['message'] == INVALID_TOKEN
        rv = post_request(client, 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXV')
        assert rv.get_json()['message'] == INVALID_TOKEN
