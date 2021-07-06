from tests.utils import request
from app.utils.exception import AuthenticationException


def get_access_token(client, credential=None):
    if credential is None:
        credential = {'username': 'tung', 'password': '123456'}
    response = request.post(client, '/login', credential)
    if response.status_code == 401:
        raise AuthenticationException
    return response.get_json()['access_token']
