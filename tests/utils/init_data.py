from app.models.category import CategoryModel
from app.models.item import ItemModel
from app.models.user import UserModel

users = [
    {
        'username': 'tung',
        'password': '123456'
    },
    {
        'username': 'btt',
        'password': '@123456'
    }
]

categories = [
    {
        'name': 'balls',
        'description': 'kick',
        'user_id': 1
    },
    {
        'name': 'books',
        'description': 'read',
        'user_id': 1
    },
    {
        'name': 'shoes',
        'description': 'wear',
        'user_id': 2
    },
    {
        'name': 'computers',
        'description': 'code',
        'user_id': 1
    }
]

items = [
    {
        'name': 'football',
        'description': 'kick',
        'user_id': 1,
        'category_id': 1,
        'price': 4.99
    },
    {
        'name': 'baseball',
        'description': 'hit',
        'user_id': 2,
        'category_id': 1,
        'price': 3.99
    }, {
        'name': 'basketball',
        'description': 'throw',
        'user_id': 1,
        'category_id': 1,
        'price': 3.99
    }, {
        'name': 'logic',
        'description': 'study',
        'user_id': 1,
        'category_id': 2,
        'price': 7.99
    }, {
        'name': 'adidas',
        'description': 'run',
        'user_id': 2,
        'category_id': 3,
        'price': 20.99
    }, {
        'name': 'mac',
        'description': 'code',
        'user_id': 1,
        'category_id': 4,
        'price': 199.99
    }
]


def init_test_data():
    for user in users:
        UserModel(**user).save()

    for category in categories:
        CategoryModel(**category).save()

    for item in items:
        ItemModel(**item).save()
