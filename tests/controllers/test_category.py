from tests.utils import token
from tests.utils import request
from app.utils.messages.message import CATEGORY_DUPLICATED, CATEGORY_NOT_FOUND, UNAUTHORIZED, INVALID_TOKEN, \
    MISSING_TOKEN


class TestGetCategory:
    def test_get_all_categories(self, client):
        rv = client.get('/categories')
        assert rv.status_code == 200
        body = rv.get_json()
        assert body['total'] == 4
        assert body['categories'][0]['name'] == 'balls'
        assert body['categories'][1]['description'] == 'read'
        assert body['categories'][2]['user_id'] == 2

    def test_get_all_categories_valid_parameter(self, client):
        rv = client.get('/categories?page=1&limit=2')
        assert rv.status_code == 200
        body = rv.get_json()
        assert body['total'] == 4
        assert len(body['categories']) == 2
        assert body['categories'][0]['name'] == 'balls'
        assert body['categories'][1]['description'] == 'read'

    def test_get_all_categories_invalid_parameter(self, client):
        rv = client.get('/categories?page=-1&limit=2')
        assert rv.status_code == 400
        rv = client.get('/categories?page=1&limit=aa')
        assert rv.status_code == 400

    def test_get_valid_category(self, client):
        rv = client.get('/categories/1')
        assert rv.status_code == 200
        body = rv.get_json()
        assert body['name'] == 'balls'
        assert body['description'] == 'kick'
        assert body['user_id'] == 1

    def test_get_invalid_category(self, client):
        rv = client.get('/categories/20')
        assert rv.status_code == 404
        assert rv.get_json()['message'] == CATEGORY_NOT_FOUND


class TestPostCategory:
    def test_insert_category_success(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': 'test_cat',
            'description': 'testing'
        }
        rv = request.post(client, '/categories', data, access_token)
        assert rv.status_code == 200
        body = rv.get_json()
        assert body['name'] == data['name']
        assert body['description'] == data['description']

    def test_insert_category_duplicated(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': 'balls',
            'description': 'testing'
        }
        rv = request.post(client, '/categories', data, access_token)
        assert rv.status_code == 409
        assert rv.get_json()['message'] == CATEGORY_DUPLICATED

    def test_insert_category_invalid_type(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': 8328421,
            'description': 11111
        }
        rv = request.post(client, '/categories', data, access_token)
        assert rv.status_code == 400

    def test_insert_category_missing_field(self, client):
        access_token = token.get_access_token(client)
        data = {
            'description': 'testing'
        }
        rv = request.post(client, '/categories', data, access_token)
        assert rv.status_code == 400

    def test_insert_category_unknown_field(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': 'unknown_cat',
            'description': 'testing',
            'price': 3000
        }
        rv = request.post(client, '/categories', data, access_token)
        assert rv.status_code == 400

    def test_insert_category_with_empty_field(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': '',
            'description': ''
        }
        rv = request.post(client, '/categories', data, access_token)
        assert rv.status_code == 400

    def test_insert_category_with_invalid_length(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': 'u' * 50,
            'description': 'testing',
        }
        rv = request.post(client, '/categories', data, access_token)
        assert rv.status_code == 400


class TestPutCategory:
    def test_update_valid_category(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': 'balls',
            'description': 'euro2021'
        }
        rv = request.put(client, '/categories/1', data, access_token)
        assert rv.status_code == 200

    def test_update_category_wrong_user(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': 'shoes',
            'description': 'running'
        }
        rv = request.put(client, '/categories/3', data, access_token)
        assert rv.status_code == 403
        assert rv.get_json()['message'] == UNAUTHORIZED

    def test_update_category_invalid_body(self, client):
        access_token = token.get_access_token(client)
        data = {
            'description': 'euro2021'
        }
        rv = request.put(client, '/categories/1', data, access_token)
        assert rv.status_code == 400


class TestDeleteCategory:
    def test_delete_category(self, client):
        access_token = token.get_access_token(client)

        rv = request.delete(client, '/categories/4', access_token)
        assert rv.status_code == 200

    def test_delete_category_unauthorized(self, client):
        access_token = token.get_access_token(client)

        rv = request.delete(client, '/categories/3', access_token)
        assert rv.status_code == 403
        assert rv.get_json()['message'] == UNAUTHORIZED


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


def post_request(client, access_token):
    data = {
        'name': 'test_cat',
        'description': 'testing'
    }
    return request.post(client, '/categories', data, access_token)
