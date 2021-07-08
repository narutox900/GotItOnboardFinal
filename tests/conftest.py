import pytest

from app import create_app
from app.db import init_db, clear_db
from tests.utils import init_data


@pytest.fixture
def client():
    app = create_app()

    with app.test_client() as client:
        with app.app_context():
            init_db()
            init_data.init_test_data()
        yield client

    with app.app_context():
        clear_db()
