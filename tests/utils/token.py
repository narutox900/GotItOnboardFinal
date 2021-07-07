from tests.utils import request


def get_access_token(client, credential=None):
    if credential is None:
        credential = {'username': 'tung', 'password': '123456'}
    response = request.post(client, '/login', credential)
    return response.get_json()['access_token']
