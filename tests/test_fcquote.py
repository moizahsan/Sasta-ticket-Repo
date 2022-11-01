from flask import url_for

from unittest import mock
from decimal import Decimal

from dsapi.extensions import pwd_context
from dsapi.models import QuoteModel, QuoteCollection


def test_get_fcquote(client, db, user, admin_headers, fcquote_object):
    # test 404
    fcquote_url = url_for('api.fcquote_by_id', id="2")
    rep = client.get(fcquote_url, headers=admin_headers)
    assert rep.status_code == 404

    # test get_fcquote
    fcquote_url = url_for('api.fcquote_by_id', id="1")
    rep = client.get(fcquote_url, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["data"]
    assert data['id'] == 1
    assert data['flight_number'] == 'PK-203'
    assert data['premium'] == 23.03
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix',mock.Mock(return_value=[('ER-524', 251, 352, 9773, 1456, 18057086.766000003, 10, 113, 14184, Decimal('0.0007050197405527354765933'), Decimal('0.1026508742244782853919910'), Decimal('0.0079667230682459108855048'), Decimal('0.00686813'), 2500)]))
def test_create_fc_quote(client, db, admin_headers):
    # test bad data
    fcquote_url = url_for('api.create_fcquote')
    data = {"flight_number": 123}
    rep = client.post(fcquote_url, json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["flight_number"] = "PK-203"

    rep = client.post(fcquote_url, json=data, headers=admin_headers)
    assert rep.status_code == 201
    assert rep.get_json()['data'] is not None
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'

    fcquote = db.session.query(QuoteModel).filter_by(flight_number=data["flight_number"]).first()

    assert fcquote.flight_number == "PK-203"
    assert fcquote.premium == rep.get_json()['data']['premium']
    assert fcquote.model_param is not None


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix',mock.Mock(return_value=[]))
def test_create_fc_quote_no_flight(client, db, admin_headers):
    # test bad data
    fcquote_url = url_for('api.create_fcquote')
    data = {"flight_number": "ER-522"}

    rep = client.post(fcquote_url, json=data, headers=admin_headers)
    assert rep.status_code == 404

    fcquote = db.session.query(QuoteModel).filter_by(flight_number=data["flight_number"]).first()

    assert fcquote is None


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix',mock.Mock(return_value=[('PK-451', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625)]))
def test_create_fc_quote_no_fc(client, db, admin_headers):
    # test bad data
    fcquote_url = url_for('api.create_fcquote')
    data = {"flight_number": "PK-451"}

    rep = client.post(fcquote_url, json=data, headers=admin_headers)
    assert rep.status_code == 201
    assert rep.get_json()['data'] is not None
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'

    fcquote = db.session.query(QuoteModel).filter_by(flight_number=data["flight_number"]).first()

    assert fcquote.flight_number == "PK-451"
    assert fcquote.premium == rep.get_json()['data']['premium']
    assert fcquote.premium >= 650 # Added by Mohib 18/05/2022. Modified to 650 4/09/2022

# V1.1 Tests below

@mock.patch('dsapi.services.calculate_premium.get_premium_matrix',mock.Mock(return_value=[('ER-524', 251, 352, 9773, 1456, 18057086.766000003, 10, 113, 14184, Decimal('0.0007050197405527354765933'), Decimal('0.1026508742244782853919910'), Decimal('0.0079667230682459108855048'), Decimal('0.00686813'), 2500)]))
def test_create_fc_quote_pax(client, db, admin_headers):
    fcquote_url = url_for('api_v11.create_fcquote_v11')
    bad_data = {"flight_number": "ER-524",
                       "param": {
                           "adult_pax": "3",
                           "child_pax": 2
                       }}

    rep = client.post(fcquote_url, json=bad_data, headers=admin_headers)
    assert rep.status_code == 400

    data = {"flight_number": "ER-524",
            "param": {
                "adult_pax": 3,
                "child_pax": 2
            }}


    rep = client.post(fcquote_url, json=data, headers=admin_headers)
    assert rep.status_code == 201
    assert rep.get_json()['data'] is not None
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'

    fcquote = db.session.query(QuoteModel).filter_by(flight_number=data["flight_number"]).first()

    assert fcquote.flight_number == "ER-524"
    assert fcquote.premium == rep.get_json()['data']['premium']
    assert fcquote.premium >= 650 # Added by Mohib 18/05/2022. Modified to 650 4/09/2022
    assert fcquote.model_param is not None
    assert fcquote.param is not None


    fcquote_url_single_pax = url_for('api.create_fcquote')
    data_single_pax = {"flight_number": "ER-524"}
    rep_single_pax = client.post(fcquote_url_single_pax, json=data_single_pax, headers=admin_headers)

    fcquote_single_pax = db.session.query(QuoteModel).filter_by(id=rep_single_pax.get_json()['data']['id']).first()
    pax_factor = fcquote.premium / fcquote_single_pax.premium
    assert 5 - pax_factor < 0.1


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix',mock.Mock(return_value=[('ER-524', 251, 352, 9773, 1456, 18057086.766000003, 10, 113, 14184, Decimal('0.0007050197405527354765933'), Decimal('0.1026508742244782853919910'), Decimal('0.0079667230682459108855048'), Decimal('0.00686813'), 2500)]))
def test_create_fc_quote_pax(client, db, admin_headers):
    # test bad data
    fcquote_url = url_for('api_v11.create_fcquote_v11')
    data = {"flight_number": 123}
    rep = client.post(fcquote_url, json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["flight_number"] = "PK-203"
    data["param"]= {
        "adult_pax": 3,
        "child_pax": 2
    }

    rep = client.post(fcquote_url, json=data, headers=admin_headers)
    assert rep.status_code == 201
    assert rep.get_json()['data'] is not None
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'

    fcquote = db.session.query(QuoteModel).filter_by(flight_number=data["flight_number"]).first()

    assert fcquote.flight_number == "PK-203"
    assert fcquote.premium == rep.get_json()['data']['premium']
    assert fcquote.premium >= 650 # Added by Mohib 18/05/2022. Modified to 650 4/09/2022
    assert fcquote.model_param is not None
    assert fcquote.param == data["param"]


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix',mock.Mock(return_value=[]))
def test_create_fc_quote_no_flight_pax(client, db, admin_headers):
    # test bad data
    fcquote_url = url_for('api_v11.create_fcquote_v11')
    data = {"flight_number": "ER-522",
            "param": {
                "adult_pax": 3,
                "child_pax": 2
            }}

    rep = client.post(fcquote_url, json=data, headers=admin_headers)
    assert rep.status_code == 404

    fcquote = db.session.query(QuoteModel).filter_by(flight_number=data["flight_number"]).first()

    assert fcquote is None


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix',mock.Mock(return_value=[('PK-451', 10, 16, 1006, 376, 3526675.142, None, None, 2054, None, Decimal('0.1830574488802336903602726'), None, None, 4625)]))
def test_create_fc_quote_no_fc_pax(client, db, admin_headers):
    # test bad data
    fcquote_url = url_for('api_v11.create_fcquote_v11')
    data = {"flight_number": "PK-451",
            "param": {
                "adult_pax": 3,
                "child_pax": 2
            }}

    rep = client.post(fcquote_url, json=data, headers=admin_headers)
    assert rep.status_code == 201
    assert rep.get_json()['data'] is not None
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'

    fcquote = db.session.query(QuoteModel).filter_by(flight_number=data["flight_number"]).first()

    assert fcquote.flight_number == "PK-451"
    assert fcquote.premium == rep.get_json()['data']['premium']
    assert fcquote.premium >= 650 # Added by Mohib 18/05/2022. Modified to 650 4/09/2022
    assert fcquote.param == data['param']
