import json


def get(client, path, token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return client.get(path, headers=headers)


def post(client, path, data, token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return client.post(path, headers=headers, data=json.dumps(data))


def put(client, path, data, token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return client.put(path, headers=headers, data=json.dumps(data))


def delete(client, path, token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return client.delete(path, headers=headers)
