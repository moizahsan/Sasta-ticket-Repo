from flask import url_for

from unittest import mock
from decimal import Decimal

from dsapi.extensions import pwd_context
from dsapi.models import QuoteModel, QuoteCollection


# V1.1

def test_get_dc_quote_multi_collection_pax(client, db, admin_headers, dcquote_collection_object_pax):
    quote_collection_url = url_for('api_v11.quote_fc_collection_by_id_v11', id = dcquote_collection_object_pax.id)

    rep = client.get(quote_collection_url, headers=admin_headers)
    assert rep.status_code == 200
    assert rep.get_json()['data'] is not None
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'
    assert len(rep.get_json()['data']['fcquotes']) == 2
    assert rep.get_json()['data']['fcquotes'][0]['param'] is not None


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix_sql', mock.Mock(return_value=[('ER-524',14,20,9899,None,None,None,None,14354,None,None,None,None,5500), ('PK-452',45,10,4578,None,None,None,None,18354,None,None,None,None,3500)]))
def test_create_dc_quote_multi_object_pax(client, db, admin_headers):
    quote_collection_url = url_for('api_v11.create_fc_quote_collection_v11')
    data = {"quote_type": "dc", "fcquotes": [{"flight_number": "ER-524", "param":{
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

    quote_collection = db.session.query(QuoteCollection).filter_by(quote_type="dc").first()

    assert len(quote_collection.fcquotes) == len(rep.get_json()['data']['fcquotes'])
    assert all(isinstance(item, QuoteModel) for item in quote_collection.fcquotes)
    assert rep.get_json()['data']['fcquotes'][0]['param'] is not None

#FIXME
@mock.patch('dsapi.services.calculate_premium.get_premium_matrix_sql', mock.Mock(return_value=[('ER-524',14,20,9899,None,None,None,None,14354,None,None,None,None,5500), ('PK-452',45,10,4578,None,None,None,None,18354,None,None,None,None,3500)]))
def test_create_dc_quote_multi_collection_pax(client, db, admin_headers):
    quote_collection_url = url_for('api_v11.create_fc_quote_collection_v11')
    data = {"quote_type": "dc", "fcquotes": [{"flight_number": "ER-524", "param":{
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

    quote_collection = db.session.query(QuoteCollection).filter_by(quote_type="dc").first()

    assert len(quote_collection.fcquotes) == 2
    assert all(isinstance(item, QuoteModel) for item in quote_collection.fcquotes)
    assert rep.get_json()['data']['fcquotes'][0]['param'] is not None


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix_sql', mock.Mock(return_value=[('ER-524',14,20,9899,None,None,None,None,14354,None,None,None,None,5500)]))
def test_create_dc_multi_quote_single_resp_collection_pax(client, db, admin_headers):
    quote_collection_url = url_for('api_v11.create_fc_quote_collection_v11')
    data = {"quote_type": "dc", "fcquotes": [{"flight_number": "ER-524", "param":{
        "adult_pax": 1,
        "child_pax": 0
    }}, {"flight_number": "PK-452", "param":{
        "adult_pax": 2,
        "child_pax": 2
    }}]}

    rep = client.post(quote_collection_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    quote_collection = db.session.query(QuoteCollection).filter_by(quote_type="dc").first()

    assert len(quote_collection.fcquotes) == 1
    assert all(isinstance(item, QuoteModel) for item in quote_collection.fcquotes)
    assert rep.get_json()['data']['fcquotes'][0]['param'] is not None


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix_sql', mock.Mock(return_value=[]))
def test_create_fc_no_quote_collection_pax(client, db, admin_headers):
    quote_collection_url = url_for('api_v11.create_fc_quote_collection_v11')
    data = {"quote_type": "dc", "fcquotes": [{"flight_number": "PK-451", "param":{
        "adult_pax": 1,
        "child_pax": 0
    }}, {"flight_number": "PK-452", "param":{
        "adult_pax": 2,
        "child_pax": 2
    }}]}

    rep = client.post(quote_collection_url, json=data, headers=admin_headers)
    assert rep.status_code == 404


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix_sql', mock.Mock(return_value=[('PK-451',14,20,9899,None,None,None,None,14354,None,None,None,None,5500)]))
def test_create_dc_single_quote_collection_pax(client, db, admin_headers):
    quote_collection_url = url_for('api_v11.create_fc_quote_collection_v11')
    data = {"quote_type": "dc", "fcquotes": [{"flight_number": "PK-451", "param":{
        "adult_pax": 1,
        "child_pax": 0
    }}]}

    rep = client.post(quote_collection_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    quote_collection = db.session.query(QuoteCollection).filter_by(quote_type="dc").first()

    assert len(quote_collection.fcquotes) == 1
    assert all(isinstance(item, QuoteModel) for item in quote_collection.fcquotes)
    assert rep.get_json()['data']['fcquotes'][0]['param'] is not None
