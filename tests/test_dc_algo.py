import pytest

from flask import url_for

from unittest import mock
from decimal import Decimal

from dsapi.extensions import pwd_context
from dsapi.models import QuoteModel, QuoteCollection, DC_Premium_Matrix


def test_single_dc_quote_calculation(client, db, admin_headers, dcquote_collection_object):
    results = [('ER-524',14,20,9899,None,None,None,None,14354,None,None,None,None,5500)]
    # results = [('ER-524', 251, 352, 9773, 1456, Decimal('18057086.766000003'), 10, 113, 14184, Decimal('0.0007050197405527354765933'), Decimal('0.1026508742244782853919910'), Decimal('0.0079667230682459108855048'), Decimal('0.00686813'), 2500)]
    premium_matrix_obj = DC_Premium_Matrix(results[0])
    premium_matrix_obj.load_param()
    premium_matrix_obj.run_algo()

    assert premium_matrix_obj.dc_participation_rate == Decimal(0.1)
    assert premium_matrix_obj.dc_exercise_rate == Decimal(0.1)
    assert premium_matrix_obj.romr == Decimal(0.05)
    assert premium_matrix_obj.sales == Decimal('2.000000000000000111022302463')
    assert premium_matrix_obj.max_risk == Decimal('11000.00000000000061062266355')
    assert premium_matrix_obj.ex_exercise_qty == Decimal('0.2000000000000000222044604926')
    assert premium_matrix_obj.tot_ex_charge == Decimal('1100.000000000000122124532709')
    assert premium_matrix_obj.net_income == Decimal('550.0000000000000610622663547')
    assert premium_matrix_obj.ex_premium_revenue == Decimal('1650.000000000000183186799064')
    assert premium_matrix_obj.premium >= 500 # Added by Mohib 18/05/2022
    assert premium_matrix_obj.premium == Decimal('825.0000000000000457966997660')


def test_single_dc_quote_no_hist_pax_calculation(client, db, admin_headers, dcquote_collection_object):
    results = [('ER-524',20,None,9899,None,None,None,None,14354,None,None,None,None,5500)]
    # results = [('ER-524', 251, 352, 9773, 1456, Decimal('18057086.766000003'), 10, 113, 14184, Decimal('0.0007050197405527354765933'), Decimal('0.1026508742244782853919910'), Decimal('0.0079667230682459108855048'), Decimal('0.00686813'), 2500)]
    premium_matrix_obj = DC_Premium_Matrix(results[0])
    premium_matrix_obj.load_param()
    premium_matrix_obj.run_algo()

    assert premium_matrix_obj.romr == Decimal(0.05)
    assert premium_matrix_obj.sales == 0
    assert premium_matrix_obj.max_risk == 0
    assert premium_matrix_obj.ex_exercise_qty == 0
    assert premium_matrix_obj.tot_ex_charge == 0
    assert premium_matrix_obj.net_income == 0
    assert premium_matrix_obj.ex_premium_revenue == 0
    assert premium_matrix_obj.premium >= 500 # Added by Mohib 18/05/2022

def test_multi_dc_quote_calculation(client, db, admin_headers):
    results = [('ER-524',14,20,9899,None,None,None,None,14354,None,None,None,None,5500),
               ('PK-452',45,10,4578,None,None,None,None,18354,None,None,None,None,3500)]

    er524_premium_matrix_obj = DC_Premium_Matrix(results[0])
    er524_premium_matrix_obj.load_param()
    er524_premium_matrix_obj.run_algo()

    pk452_premium_matrix_obj = DC_Premium_Matrix(results[1])
    pk452_premium_matrix_obj.load_param()
    pk452_premium_matrix_obj.run_algo()

    premium_matrix_obj = DC_Premium_Matrix(results)
    premium_matrix_obj.load_param_matrix()
    premium_matrix_obj.run_matrix_algo()


    assert abs(er524_premium_matrix_obj.dc_participation_rate - Decimal(premium_matrix_obj.matrix[0][14])) < 0.0001
    assert abs(er524_premium_matrix_obj.dc_exercise_rate - Decimal(premium_matrix_obj.matrix[0][9])) < 0.0001
    assert abs(er524_premium_matrix_obj.romr - Decimal(premium_matrix_obj.matrix[0][15])) < 0.0001
    assert abs(er524_premium_matrix_obj.sales - Decimal(premium_matrix_obj.matrix[0][16])) < 0.0001
    assert abs(er524_premium_matrix_obj.max_risk - Decimal(premium_matrix_obj.matrix[0][17])) < 0.0001
    assert abs(er524_premium_matrix_obj.ex_exercise_qty - Decimal(premium_matrix_obj.matrix[0][18])) < 0.0001
    assert abs(er524_premium_matrix_obj.tot_ex_charge - Decimal(premium_matrix_obj.matrix[0][19])) < 0.0001
    assert abs(er524_premium_matrix_obj.net_income - Decimal(premium_matrix_obj.matrix[0][20])) < 0.0001
    assert abs(er524_premium_matrix_obj.ex_premium_revenue - Decimal(premium_matrix_obj.matrix[0][21])) < 0.0001
    assert abs(er524_premium_matrix_obj.premium - Decimal(premium_matrix_obj.matrix[0][22])) < 0.0001

    assert abs(pk452_premium_matrix_obj.dc_participation_rate - Decimal(premium_matrix_obj.matrix[1][14])) < 0.0001
    assert abs(pk452_premium_matrix_obj.dc_exercise_rate - Decimal(premium_matrix_obj.matrix[1][9])) < 0.0001
    assert abs(pk452_premium_matrix_obj.romr - Decimal(premium_matrix_obj.matrix[1][15])) < 0.0001
    assert abs(pk452_premium_matrix_obj.sales - Decimal(premium_matrix_obj.matrix[1][16])) < 0.0001
    assert abs(pk452_premium_matrix_obj.max_risk - Decimal(premium_matrix_obj.matrix[1][17])) < 0.0001
    assert abs(pk452_premium_matrix_obj.ex_exercise_qty - Decimal(premium_matrix_obj.matrix[1][18])) < 0.0001
    assert abs(pk452_premium_matrix_obj.tot_ex_charge - Decimal(premium_matrix_obj.matrix[1][19])) < 0.0001
    assert abs(pk452_premium_matrix_obj.net_income - Decimal(premium_matrix_obj.matrix[1][20])) < 0.0001
    assert abs(pk452_premium_matrix_obj.ex_premium_revenue - Decimal(premium_matrix_obj.matrix[1][21])) < 0.0001
    assert abs(pk452_premium_matrix_obj.premium - Decimal(premium_matrix_obj.matrix[1][22])) < 0.0001
    assert abs(pk452_premium_matrix_obj.premium) >= 500 # Added by Mohib 18/05/2022


def test_single_dc_quote_calculation_pax(client, db, admin_headers, dcquote_collection_object, dcquote_object_pax):
    results = [('ER-524',14,20,9899,None,None,None,None,14354,None,None,None,None,5500)]
    # results = [('ER-524', 251, 352, 9773, 1456, Decimal('18057086.766000003'), 10, 113, 14184, Decimal('0.0007050197405527354765933'), Decimal('0.1026508742244782853919910'), Decimal('0.0079667230682459108855048'), Decimal('0.00686813'), 2500)]
    premium_matrix_obj = DC_Premium_Matrix(results[0])
    premium_matrix_obj.load_param(dcquote_object_pax)
    premium_matrix_obj.run_algo()

    assert premium_matrix_obj.dc_participation_rate == Decimal(0.1)
    assert premium_matrix_obj.dc_exercise_rate == Decimal(0.1)
    assert premium_matrix_obj.romr == Decimal(0.05)
    assert premium_matrix_obj.sales == Decimal('2.000000000000000111022302463')
    assert premium_matrix_obj.max_risk == Decimal('11000.00000000000061062266355')
    assert premium_matrix_obj.ex_exercise_qty == Decimal('0.2000000000000000222044604926')
    assert premium_matrix_obj.tot_ex_charge == Decimal('1100.000000000000122124532709')
    assert premium_matrix_obj.net_income == Decimal('550.0000000000000610622663547')
    assert premium_matrix_obj.ex_premium_revenue == Decimal('1650.000000000000183186799064')
    assert premium_matrix_obj.premium >= 500*3 # fcquote_object_pax has set 2 adult pax + 1 child pax for this flight # Added by Mohib 18/05/2022
    assert premium_matrix_obj.premium == Decimal('825.0000000000000457966997660')*3


def test_multi_dc_quote_calculation_pax(client, db, admin_headers, dcquote_collection_schema_pax):
    results = [('ER-524',14,20,9899,None,None,None,None,14354,None,None,None,None,5500),
               ('PK-452',45,10,4578,None,None,None,None,18354,None,None,None,None,3500)]

    er524_premium_matrix_obj = DC_Premium_Matrix(results[0])
    er524_premium_matrix_obj.load_param()
    er524_premium_matrix_obj.run_algo()

    pk452_premium_matrix_obj = DC_Premium_Matrix(results[1])
    pk452_premium_matrix_obj.load_param()
    pk452_premium_matrix_obj.run_algo()

    premium_matrix_obj = DC_Premium_Matrix(results)
    premium_matrix_obj.load_param_matrix(dcquote_collection_schema_pax)
    premium_matrix_obj.run_matrix_algo()

    assert abs(er524_premium_matrix_obj.dc_participation_rate - Decimal(premium_matrix_obj.matrix[0][14])) < 0.0001
    assert abs(er524_premium_matrix_obj.dc_exercise_rate - Decimal(premium_matrix_obj.matrix[0][9])) < 0.0001
    assert abs(er524_premium_matrix_obj.romr - Decimal(premium_matrix_obj.matrix[0][15])) < 0.0001
    assert abs(er524_premium_matrix_obj.sales - Decimal(premium_matrix_obj.matrix[0][16])) < 0.0001
    assert abs(er524_premium_matrix_obj.max_risk - Decimal(premium_matrix_obj.matrix[0][17])) < 0.0001
    assert abs(er524_premium_matrix_obj.ex_exercise_qty - Decimal(premium_matrix_obj.matrix[0][18])) < 0.0001
    assert abs(er524_premium_matrix_obj.tot_ex_charge - Decimal(premium_matrix_obj.matrix[0][19])) < 0.0001
    assert abs(er524_premium_matrix_obj.net_income - Decimal(premium_matrix_obj.matrix[0][20])) < 0.0001
    assert abs(er524_premium_matrix_obj.ex_premium_revenue - Decimal(premium_matrix_obj.matrix[0][21])) < 0.0001
    assert abs(er524_premium_matrix_obj.premium * 2 - Decimal(premium_matrix_obj.matrix[0][22])) < 0.0001 # dcquote_collection_schema_pax has set 2 adult pax for this flight

    assert abs(pk452_premium_matrix_obj.dc_participation_rate - Decimal(premium_matrix_obj.matrix[1][14])) < 0.0001
    assert abs(pk452_premium_matrix_obj.dc_exercise_rate - Decimal(premium_matrix_obj.matrix[1][9])) < 0.0001
    assert abs(pk452_premium_matrix_obj.romr - Decimal(premium_matrix_obj.matrix[1][15])) < 0.0001
    assert abs(pk452_premium_matrix_obj.sales - Decimal(premium_matrix_obj.matrix[1][16])) < 0.0001
    assert abs(pk452_premium_matrix_obj.max_risk - Decimal(premium_matrix_obj.matrix[1][17])) < 0.0001
    assert abs(pk452_premium_matrix_obj.ex_exercise_qty - Decimal(premium_matrix_obj.matrix[1][18])) < 0.0001
    assert abs(pk452_premium_matrix_obj.tot_ex_charge - Decimal(premium_matrix_obj.matrix[1][19])) < 0.0001
    assert abs(pk452_premium_matrix_obj.net_income - Decimal(premium_matrix_obj.matrix[1][20])) < 0.0001
    assert abs(pk452_premium_matrix_obj.ex_premium_revenue - Decimal(premium_matrix_obj.matrix[1][21])) < 0.0001
    assert abs(pk452_premium_matrix_obj.premium*3 - Decimal(premium_matrix_obj.matrix[1][22])) < 0.0001 # dcquote_collection_schema_pax has set 1 adult pax + 2 child pax for this flight
    assert abs(pk452_premium_matrix_obj.premium) >= 500
