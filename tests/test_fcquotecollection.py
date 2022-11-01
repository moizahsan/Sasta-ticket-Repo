from flask import url_for

from unittest import mock
from decimal import Decimal

from dsapi.extensions import pwd_context
from dsapi.models import QuoteModel, QuoteCollection


def test_get_fc_quote_multi_collection(client, db, admin_headers, fcquote_collection_object):
    quote_collection_url = url_for('api.quote_collection_by_id', id = fcquote_collection_object.id)

    rep = client.get(quote_collection_url, headers=admin_headers)
    assert rep.status_code == 200
    assert rep.get_json()['data'] is not None
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'
    assert len(rep.get_json()['data']['fcquotes']) == 2


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix_sql', mock.Mock(return_value=[('PK-451', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625), ('PK-452', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625)]))
@mock.patch('dsapi.services.calculate_premium.get_premium_matrix',mock.Mock(return_value=[('PK-451', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625)]))
def test_create_fc_quote_multi_object(client, db, admin_headers):
    quote_collection_url = url_for('api.create_quote_collection')
    data = {"quote_type": "fc", "fcquotes": [{"flight_number": "PK-451"}, {"flight_number": "PK-452"}]}

    rep = client.post(quote_collection_url, json=data, headers=admin_headers)
    assert rep.status_code == 201
    assert rep.get_json()['data'] is not None
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'

    quote_collection = db.session.query(QuoteCollection).filter_by(quote_type="fc").first()

    assert len(quote_collection.fcquotes) == len(rep.get_json()['data']['fcquotes'])
    assert all(isinstance(item, QuoteModel) for item in quote_collection.fcquotes)

    data_pk451 = {"flight_number": "PK-451"}
    data_pk452 = {"flight_number": "PK-452"}

    quote_url = url_for('api.create_fcquote')
    rep_451 = client.post(quote_url, json=data_pk451, headers=admin_headers)

    assert rep.get_json()['data']['fcquotes'][0]['premium'] == rep_451.get_json()['data']['premium']


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix_sql', mock.Mock(return_value=[('PK-451', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625), ('PK-452', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625)]))
def test_create_fc_quote_multi_collection(client, db, admin_headers):
    quote_collection_url = url_for('api.create_quote_collection')
    data = {"quote_type": "fc", "fcquotes": [{"flight_number": "PK-451"}, {"flight_number": "PK-452"}]}

    rep = client.post(quote_collection_url, json=data, headers=admin_headers)
    assert rep.status_code == 201
    assert rep.get_json()['data'] is not None
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'

    quote_collection = db.session.query(QuoteCollection).filter_by(quote_type="fc").first()

    assert len(quote_collection.fcquotes) == 2
    assert all(isinstance(item, QuoteModel) for item in quote_collection.fcquotes)


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix_sql', mock.Mock(return_value=[('PK-451', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625)]))
@mock.patch('dsapi.services.calculate_premium.get_premium_matrix',mock.Mock(return_value=[('PK-451', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625)]))
def test_create_fc_multi_quote_single_resp_collection(client, db, admin_headers):
    quote_collection_url = url_for('api.create_quote_collection')
    data = {"quote_type": "fc", "fcquotes": [{"flight_number": "PK-451"}, {"flight_number": "PK-678"}]}

    rep = client.post(quote_collection_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    quote_collection = db.session.query(QuoteCollection).filter_by(quote_type="fc").first()

    assert len(quote_collection.fcquotes) == 1
    assert all(isinstance(item, QuoteModel) for item in quote_collection.fcquotes)

    data_pk451 = {"flight_number": "PK-451"}

    quote_url = url_for('api.create_fcquote')
    rep_451 = client.post(quote_url, json=data_pk451, headers=admin_headers)

    assert rep.get_json()['data']['fcquotes'][0]['premium'] == rep_451.get_json()['data']['premium']


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix_sql', mock.Mock(return_value=[]))
def test_create_fc_no_quote_collection(client, db, admin_headers):
    quote_collection_url = url_for('api.create_quote_collection')
    data = {"quote_type": "fc", "fcquotes": [{"flight_number": "PK-451"}, {"flight_number": "PK-678"}]}

    rep = client.post(quote_collection_url, json=data, headers=admin_headers)
    assert rep.status_code == 404


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix_sql', mock.Mock(return_value=[('PK-451', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625)]))
@mock.patch('dsapi.services.calculate_premium.get_premium_matrix',mock.Mock(return_value=[('PK-451', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625)]))
def test_create_fc_single_quote_collection(client, db, admin_headers):
    quote_collection_url = url_for('api.create_quote_collection')
    data = {"quote_type": "fc", "fcquotes": [{"flight_number": "PK-451"}]}

    rep = client.post(quote_collection_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    quote_collection = db.session.query(QuoteCollection).filter_by(quote_type="fc").first()

    assert len(quote_collection.fcquotes) == 1
    assert all(isinstance(item, QuoteModel) for item in quote_collection.fcquotes)

# V1.1

def test_get_fc_quote_multi_collection_pax(client, db, admin_headers, fcquote_collection_object_pax):
    quote_collection_url = url_for('api_v11.quote_fc_collection_by_id_v11', id = fcquote_collection_object_pax.id)

    rep = client.get(quote_collection_url, headers=admin_headers)
    assert rep.status_code == 200
    assert rep.get_json()['data'] is not None
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'
    assert len(rep.get_json()['data']['fcquotes']) == 2
    assert rep.get_json()['data']['fcquotes'][0]['param'] is not None

#FIXME
@mock.patch('dsapi.services.calculate_premium.get_premium_matrix_sql', mock.Mock(return_value=[('PK-451', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625), ('PK-452', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625)]))
def test_create_fc_quote_multi_object_pax(client, db, admin_headers):
    quote_collection_url = url_for('api_v11.create_fc_quote_collection_v11')
    data = {"quote_type": "fc", "fcquotes": [{"flight_number": "PK-451", "param":{
        "adult_pax": 1,
        "child_pax": 0
    }}, {"flight_number": "PK-452", "param":{
        "adult_pax": 2,
        "child_pax": 2
    }}]}

    rep = client.post(quote_collection_url, json=data, headers=admin_headers)
    assert rep.status_code == 201
    assert rep.get_json()['data'] is not None
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'

    quote_collection = db.session.query(QuoteCollection).filter_by(quote_type="fc").first()

    assert len(quote_collection.fcquotes) == len(rep.get_json()['data']['fcquotes'])
    assert all(isinstance(item, QuoteModel) for item in quote_collection.fcquotes)
    assert rep.get_json()['data']['fcquotes'][0]['param'] is not None


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix_sql', mock.Mock(return_value=[('PK-451', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625), ('PK-452', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625)]))
def test_create_fc_quote_multi_collection_pax(client, db, admin_headers):
    quote_collection_url = url_for('api_v11.create_fc_quote_collection_v11')
    data = {"quote_type": "fc", "fcquotes": [{"flight_number": "PK-451", "param":{
        "adult_pax": 1,
        "child_pax": 0
    }}, {"flight_number": "PK-452", "param":{
        "adult_pax": 2,
        "child_pax": 2
    }}]}

    rep = client.post(quote_collection_url, json=data, headers=admin_headers)
    assert rep.status_code == 201
    assert rep.get_json()['data'] is not None
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'

    quote_collection = db.session.query(QuoteCollection).filter_by(quote_type="fc").first()

    assert len(quote_collection.fcquotes) == 2
    assert all(isinstance(item, QuoteModel) for item in quote_collection.fcquotes)
    assert rep.get_json()['data']['fcquotes'][0]['param'] is not None


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix_sql', mock.Mock(return_value=[('PK-451', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625)]))
def test_create_fc_multi_quote_single_resp_collection_pax(client, db, admin_headers):
    quote_collection_url = url_for('api_v11.create_fc_quote_collection_v11')
    data = {"quote_type": "fc", "fcquotes": [{"flight_number": "PK-451", "param":{
        "adult_pax": 1,
        "child_pax": 0
    }}, {"flight_number": "PK-452", "param":{
        "adult_pax": 2,
        "child_pax": 2
    }}]}

    rep = client.post(quote_collection_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    quote_collection = db.session.query(QuoteCollection).filter_by(quote_type="fc").first()

    assert len(quote_collection.fcquotes) == 1
    assert all(isinstance(item, QuoteModel) for item in quote_collection.fcquotes)
    assert rep.get_json()['data']['fcquotes'][0]['param'] is not None


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix_sql', mock.Mock(return_value=[]))
def test_create_fc_no_quote_collection_pax(client, db, admin_headers):
    quote_collection_url = url_for('api_v11.create_fc_quote_collection_v11')
    data = {"quote_type": "fc", "fcquotes": [{"flight_number": "PK-451", "param":{
        "adult_pax": 1,
        "child_pax": 0
    }}, {"flight_number": "PK-452", "param":{
        "adult_pax": 2,
        "child_pax": 2
    }}]}

    rep = client.post(quote_collection_url, json=data, headers=admin_headers)
    assert rep.status_code == 404


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix_sql', mock.Mock(return_value=[('PK-451', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625)]))
def test_create_fc_single_quote_collection_pax(client, db, admin_headers):
    quote_collection_url = url_for('api_v11.create_fc_quote_collection_v11')
    data = {"quote_type": "fc", "fcquotes": [{"flight_number": "PK-451", "param":{
        "adult_pax": 1,
        "child_pax": 0
    }}]}

    rep = client.post(quote_collection_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    quote_collection = db.session.query(QuoteCollection).filter_by(quote_type="fc").first()

    assert len(quote_collection.fcquotes) == 1
    assert all(isinstance(item, QuoteModel) for item in quote_collection.fcquotes)
    assert rep.get_json()['data']['fcquotes'][0]['param'] is not None
