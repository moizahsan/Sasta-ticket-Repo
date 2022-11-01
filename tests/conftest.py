import json
import pytest
from dotenv import load_dotenv

from dsapi.models import User, QuoteModel, QuoteCollection
from dsapi.api.schemas import QuoteCollectionSchemaV11
from dsapi.app import create_app
from dsapi.extensions import db as _db
from pytest_factoryboy import register
from tests.factories import UserFactory


register(UserFactory)


@pytest.fixture(scope="session")
def app():
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = User(
        username='admin',
        email='admin@admin.com',
        password='admin'
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def admin_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['access_token']
    }


@pytest.fixture
def admin_refresh_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['refresh_token']
    }

@pytest.fixture
def fcquote_object(db):
    fcquote = QuoteModel(
        id=1,
        flight_number='PK-203',
        premium=23.03,
        quote_type='fc',
    )

    db.session.add(fcquote)
    db.session.commit()

    return fcquote


@pytest.fixture
def fcquote_object_pax(db):
    fcquote = QuoteModel(
        flight_number='PK-203',
        quote_type='fc',
        param={
            'adult_pax': 2,
            'child_pax': 1
        }
    )

    return fcquote


@pytest.fixture
def fcquote_collection_object(db):
    quote_collection = QuoteCollection(id=1, quote_type='fc')
    fcquote = QuoteModel(
        id=1,
        collection_id=1,
        flight_number='PK-203',
        premium=23.03
    )
    fcquote_1 = QuoteModel(
        id=2,
        collection_id=1,
        flight_number='PK-203',
        premium=23.03
    )
    quote_collection.fcquotes.append(fcquote)
    quote_collection.fcquotes.append(fcquote_1)


    db.session.add(fcquote)
    db.session.add(fcquote_1)
    db.session.add(quote_collection)
    db.session.commit()

    return fcquote


@pytest.fixture
def fcquote_collection_object_pax(db):
    quote_collection = QuoteCollection(id=1, quote_type='fc')
    fcquote = QuoteModel(
        id=1,
        collection_id=1,
        flight_number='PK-203',
        premium=23.03,
        quote_type='fc',
        param={
            'adult_pax': 1,
            'child_pax': 0
        }
    )
    fcquote_1 = QuoteModel(
        id=2,
        collection_id=1,
        flight_number='PK-203',
        premium=23.03,
        quote_type='fc',
        param={
            'adult_pax': 1,
            'child_pax': 0
        }
    )
    quote_collection.fcquotes.append(fcquote)
    quote_collection.fcquotes.append(fcquote_1)


    db.session.add(fcquote)
    db.session.add(fcquote_1)
    db.session.add(quote_collection)
    db.session.commit()

    return fcquote


@pytest.fixture
def fcquote_collection_schema_pax(db):
    schema = QuoteCollectionSchemaV11()
    quote_collection_schema = schema.load(
        {
            "quote_type": "fc",
            "fcquotes": [
                {
                    "flight_number": "ER-524",
                    "param": {
                        "adult_pax": 2,
                        "child_pax":0}
                },
                {
                    "flight_number": "PK-452",
                    "param": {
                        "adult_pax": 1,
                        "child_pax":2}
                    }
                ]

        })
    return quote_collection_schema


@pytest.fixture
def dcquote_object(db):
    dcquote = QuoteModel(
        id=1,
        flight_number='PK-203',
        premium=23.03,
        quote_type='dc',
    )

    db.session.add(dcquote)
    db.session.commit()

    return dcquote


@pytest.fixture
def dcquote_object_pax(db):
    dcquote = QuoteModel(
        flight_number='PK-203',
        quote_type='dc',
        param={
            'adult_pax': 2,
            'child_pax': 1
        }
    )

    return dcquote


@pytest.fixture
def dcquote_collection_object(db):
    quote_collection = QuoteCollection(id=1, quote_type='dc')
    dcquote = QuoteModel(
        id=1,
        collection_id=1,
        flight_number='PK-203',
        premium=23.03
    )
    dcquote_1 = QuoteModel(
        id=2,
        collection_id=1,
        flight_number='PK-203',
        premium=23.03
    )
    quote_collection.fcquotes.append(dcquote)
    quote_collection.fcquotes.append(dcquote_1)


    db.session.add(dcquote)
    db.session.add(dcquote_1)
    db.session.add(quote_collection)
    db.session.commit()

    return dcquote


@pytest.fixture
def dcquote_collection_object_pax(db):
    quote_collection = QuoteCollection(id=1, quote_type='dc')
    dcquote = QuoteModel(
        id=1,
        collection_id=1,
        flight_number='PK-203',
        premium=23.03,
        quote_type='dc',
        param={
            'adult_pax': 1,
            'child_pax': 0
        }
    )
    dcquote_1 = QuoteModel(
        id=2,
        collection_id=1,
        flight_number='PK-203',
        premium=23.03,
        quote_type='dc',
        param={
            'adult_pax': 1,
            'child_pax': 0
        }
    )
    quote_collection.fcquotes.append(dcquote)
    quote_collection.fcquotes.append(dcquote_1)


    db.session.add(dcquote)
    db.session.add(dcquote_1)
    db.session.add(quote_collection)
    db.session.commit()

    return dcquote


@pytest.fixture
def dcquote_collection_schema_pax(db):
    schema = QuoteCollectionSchemaV11()
    quote_collection_schema = schema.load(
        {
            "quote_type": "dc",
            "fcquotes": [
                {
                    "flight_number": "ER-524",
                    "param": {
                        "adult_pax": 2,
                        "child_pax":0}
                },
                {
                    "flight_number": "PK-452",
                    "param": {
                        "adult_pax": 1,
                        "child_pax":2}
                    }
                ]

        })
    return quote_collection_schema
