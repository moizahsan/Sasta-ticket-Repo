from flask import url_for

from unittest import mock
from decimal import Decimal

from dsapi.extensions import pwd_context
from dsapi.models import QuoteModel, QuoteCollection


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix',mock.Mock(return_value=[('ER-524',14,20,9899,None,None,None,None,14354,None,None,None,None,5500)]))
def test_create_dc_quote_pax(client, db, admin_headers):
    dcquote_url = url_for('api_v11.create_dcquote_v11')
    bad_data = {"flight_number": "ER-524",
                       "param": {
                           "adult_pax": "3",
                           "child_pax": 2
                       }}

    rep = client.post(dcquote_url, json=bad_data, headers=admin_headers)
    assert rep.status_code == 400

    data = {"flight_number": "ER-524",
            "param": {
                "adult_pax": 3,
                "child_pax": 2
            }}


    rep = client.post(dcquote_url, json=data, headers=admin_headers)
    assert rep.status_code == 201
    assert rep.get_json()['data'] is not None
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'

    dcquote = db.session.query(QuoteModel).filter_by(flight_number=data["flight_number"]).first()

    assert dcquote.flight_number == "ER-524"
    assert dcquote.premium == rep.get_json()['data']['premium']
    assert dcquote.premium >= 500 # Added by Mohib 18/05/2022
    assert dcquote.model_param is not None
    assert dcquote.param is not None


    dcquote_url_single_pax = url_for('api.create_dcquote')
    data_single_pax = {"flight_number": "ER-524"}
    rep_single_pax = client.post(dcquote_url_single_pax, json=data_single_pax, headers=admin_headers)

    dcquote_single_pax = db.session.query(QuoteModel).filter_by(id=rep_single_pax.get_json()['data']['id']).first()
    pax_factor = dcquote.premium / dcquote_single_pax.premium
    assert 5 - pax_factor < 0.1


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix',mock.Mock(return_value=[('ER-524',14,20,9899,None,None,None,None,14354,None,None,None,None,5500)]))
def test_create_dc_quote_pax(client, db, admin_headers):
    # test bad data
    dcquote_url = url_for('api_v11.create_dcquote_v11')
    data = {"flight_number": 123}
    rep = client.post(dcquote_url, json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["flight_number"] = "ER-524"
    data["param"]= {
        "adult_pax": 3,
        "child_pax": 2
    }

    rep = client.post(dcquote_url, json=data, headers=admin_headers)
    assert rep.status_code == 201
    assert rep.get_json()['data'] is not None
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'

    dcquote = db.session.query(QuoteModel).filter_by(flight_number=data["flight_number"]).first()

    assert dcquote.flight_number == "ER-524"
    assert dcquote.premium == rep.get_json()['data']['premium']
    assert dcquote.premium >= 500 # Added by Mohib 18/05/2022
    assert dcquote.model_param is not None
    assert dcquote.param == data["param"]


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix',mock.Mock(return_value=[]))
def test_create_dc_quote_no_flight_pax(client, db, admin_headers):
    # test bad data
    dcquote_url = url_for('api_v11.create_dcquote_v11')
    data = {"flight_number": "ER-522",
            "param": {
                "adult_pax": 3,
                "child_pax": 2
            }}

    rep = client.post(dcquote_url, json=data, headers=admin_headers)
    assert rep.status_code == 404

    dcquote = db.session.query(QuoteModel).filter_by(flight_number=data["flight_number"]).first()

    assert dcquote is None


@mock.patch('dsapi.services.calculate_premium.get_premium_matrix',mock.Mock(return_value=[('ER-524',14,0,9899,None,None,None,None,14354,None,None,None,None,5500)]))
def test_create_dc_quote_no_fc_pax(client, db, admin_headers):
    # test bad data
    dcquote_url = url_for('api_v11.create_dcquote_v11')
    data = {"flight_number": "ER-524",
            "param": {
                "adult_pax": 3,
                "child_pax": 2
            }}

    rep = client.post(dcquote_url, json=data, headers=admin_headers)
    assert rep.status_code == 201
    assert rep.get_json()['data'] is not None
    assert rep.get_json()['success'] == True
    assert rep.get_json()['message'] == 'Operation Successful'

    dcquote = db.session.query(QuoteModel).filter_by(flight_number=data["flight_number"]).first()

    assert dcquote.flight_number == "ER-524"
    assert dcquote.premium == rep.get_json()['data']['premium']
    assert dcquote.premium >= 500 # Added by Mohib 18/05/2022
    assert dcquote.param == data['param']
