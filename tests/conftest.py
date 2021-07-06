import pytest

from app import create_app
from app import db
from tests.utils import init_data


@pytest.fixture
def client():
    app = create_app(test_config=True)

    with app.test_client() as client:
        with app.app_context():
            db.init_db()
            init_data.init_test_data()
        yield client

    with app.app_context():
        db.clear_db()
