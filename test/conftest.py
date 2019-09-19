import pytest
from forum.app import app as test_app, db as test_db


@pytest.fixture
def db():
    test_db.create_all()
    yield test_db
    test_db.session.rollback()
    test_db.session.remove()
    test_db.drop_all()


@pytest.fixture
def client(db):
    client = test_app.test_client()
    yield client
