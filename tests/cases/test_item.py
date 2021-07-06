from tests.utils import token
from tests.utils import request


class TestGetItem:
    def test_get_all_items(self, client):
        rv = client.get('/items')
        assert rv.status_code == 200
        assert rv.get_json()['total'] == 6

    def test_get_all_items_of_category(self, client):
        rv = client.get('/categories/1/items')
        assert rv.status_code == 200
        assert rv.get_json()['total'] == 3

    def test_get_all_items_valid_parameter(self, client):
        rv = client.get('/items?page=1&limit=2')
        assert rv.status_code == 200
        body = rv.get_json()
        assert body['total'] == 6
        assert len(body['items']) == 2

    def test_get_all_items_of_category_valid_parameter(self, client):
        rv = client.get('/categories/1/items?page=1&limit=2')
        assert rv.status_code == 200
        body = rv.get_json()
        assert body['total'] == 3
        assert len(body['items']) == 2

    def test_get_all_items_invalid_parameter(self, client):
        rv = client.get('/items?page=-1&limit=2')
        assert rv.status_code == 400
        rv = client.get('/items?page=1&limit=aa')
        assert rv.status_code == 400

    def test_get_valid_item(self, client):
        rv = client.get('/categories/1/items/1')
        assert rv.status_code == 200
        body = rv.get_json()
        body = body['item']
        assert body['name'] == 'football'
        assert body['description'] == 'kick'
        assert body['user_id'] == 1
        assert body['category_id'] == 1
        assert body['price'] == 4.99

    def test_get_invalid_item(self, client):
        rv = client.get('/categories/1/items/20')
        assert rv.status_code == 404


class TestPostCategory:
    def test_insert_item_success(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': 'test_cat',
            'description': 'testing',
            'price': 20.22
        }
        rv = request.post(client, '/categories/1/items', data, access_token)
        assert rv.status_code == 200
        body = rv.get_json()
        body = body['item']
        assert body['name'] == data['name']
        assert body['description'] == data['description']
        assert body['price'] == data['price']
        assert body['category_id'] == 1

    def test_insert_item_duplicated(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': 'football',
            'description': 'testing',
            'price': 20.22
        }
        rv = request.post(client, '/categories/1/items', data, access_token)
        assert rv.status_code == 409

    def test_insert_item_invalid_type(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': 8328421,
            'description': 11111,
            'price': 'test'
        }
        rv = request.post(client, '/categories/1/items', data, access_token)
        assert rv.status_code == 400

    def test_insert_item_missing_field(self, client):
        access_token = token.get_access_token(client)
        data = {
            'description': 'testing'
        }
        rv = request.post(client, '/categories/2/items', data, access_token)
        assert rv.status_code == 400

    def test_insert_item_unknown_field(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': 'unknown_cat',
            'description': 'testing',
            'year': 2077
        }
        rv = request.post(client, '/categories/1/items', data, access_token)
        assert rv.status_code == 400

    def test_insert_item_with_empty_field(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': '',
            'description': '',
            'price': ''
        }
        rv = request.post(client, '/categories/1/items', data, access_token)
        assert rv.status_code == 400

    def test_insert_item_with_invalid_length(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': 'u' * 50,
            'description': 'testing',
            'price': 20
        }
        rv = request.post(client, '/categories/1/items', data, access_token)
        assert rv.status_code == 400


class TestPutCategory:
    def test_update_valid_item(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': 'football',
            'description': 'kicker',
            'price': 10
        }
        rv = request.put(client, '/categories/1/items/1', data, access_token)
        assert rv.status_code == 200
        body = rv.get_json()
        body = body['item']
        assert body['name'] == data['name']
        assert body['description'] == data['description']
        assert body['price'] == data['price']

    def test_update_item_wrong_user(self, client):
        access_token = token.get_access_token(client)
        data = {
            'name': 'baseball',
            'description': 'running',
            'price': 20
        }
        rv = request.put(client, '/categories/1/items/2', data, access_token)
        assert rv.status_code == 403

    def test_update_item_invalid_body(self, client):
        access_token = token.get_access_token(client)
        data = {
            'description': 'euro2021'
        }
        rv = request.put(client, 'categories/1/items/1', data, access_token)
        assert rv.status_code == 400


class TestDeleteCategory:
    def test_delete_item(self, client):
        access_token = token.get_access_token(client)

        rv = request.delete(client, '/categories/1/items/1', access_token)
        assert rv.status_code == 200

    def test_delete_item_unauthorized(self, client):
        access_token = token.get_access_token(client)

        rv = request.delete(client, '/categories/1/items/2', access_token)
        assert rv.status_code == 403
