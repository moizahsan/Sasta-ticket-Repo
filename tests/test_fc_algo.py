import pytest

from flask import url_for

from unittest import mock
from decimal import Decimal

from dsapi.extensions import pwd_context
from dsapi.models import QuoteModel, QuoteCollection, Premium_Matrix, FC_Premium_Matrix


def test_single_fc_quote_calculation(client, db, admin_headers, fcquote_collection_object):
    results = [('ER-524',119,148,9899,1480,Decimal('1.8512450281000003'),17,124,14354,Decimal('0.0011843388602480144907343'),Decimal('0.1031071478333565556639264'),Decimal('0.0086387069806325762853560'),Decimal('0.01148649'),2500)]
    # results = [('ER-524', 251, 352, 9773, 1456, Decimal('18057086.766000003'), 10, 113, 14184, Decimal('0.0007050197405527354765933'), Decimal('0.1026508742244782853919910'), Decimal('0.0079667230682459108855048'), Decimal('0.00686813'), 2500)]
    premium_matrix_obj = FC_Premium_Matrix(results[0])
    premium_matrix_obj.load_param()
    premium_matrix_obj.run_algo()

    assert premium_matrix_obj.fc_participation_rate == Decimal('0.008638706980632576285355998328')
    assert premium_matrix_obj.PTCFactor == Decimal('0.01148649')
    assert premium_matrix_obj.fc_exercise_rate == Decimal('0.0011843388602480144907343')
    assert premium_matrix_obj.romr == Decimal(0.05)
    assert premium_matrix_obj.sales == Decimal('1.278528633133621290232687753')
    assert premium_matrix_obj.max_risk == Decimal('3196.321582834053225581719382')
    assert premium_matrix_obj.ex_exercise_qty == Decimal('0.001514211144159924894381766310')
    assert premium_matrix_obj.tot_ex_charge == Decimal('3.785527860399812235954415775')
    assert premium_matrix_obj.net_income == Decimal('159.8160791417026701506605075')
    assert premium_matrix_obj.ex_premium_revenue == Decimal('163.6016070021024823866149233')
    assert premium_matrix_obj.premium >= 500 # Added by Mohib 18/05/2022.


def test_single_fc_quote_no_hist_pax_calculation(client, db, admin_headers, fcquote_collection_object):
    results = [('ER-524',None,None,9899,1480,Decimal('1.8512450281000003'),None,None,14354,None,Decimal('0.1031071478333565556639264'),None,None,2500)]
    # results = [('ER-524', 251, 352, 9773, 1456, Decimal('18057086.766000003'), 10, 113, 14184, Decimal('0.0007050197405527354765933'), Decimal('0.1026508742244782853919910'), Decimal('0.0079667230682459108855048'), Decimal('0.00686813'), 2500)]
    premium_matrix_obj = FC_Premium_Matrix(results[0])
    premium_matrix_obj.load_param()
    premium_matrix_obj.run_algo()

    assert premium_matrix_obj.PTCFactor == Decimal(3)
    assert premium_matrix_obj.romr == Decimal(0.05)
    assert premium_matrix_obj.sales == 0
    assert premium_matrix_obj.max_risk == 0
    assert premium_matrix_obj.ex_exercise_qty == 0
    assert premium_matrix_obj.tot_ex_charge == 0
    assert premium_matrix_obj.net_income == 0
    assert premium_matrix_obj.ex_premium_revenue == 0
    assert premium_matrix_obj.premium >= 500 # Added by Mohib 18/05/2022.


def test_multi_fc_quote_calculation(client, db, admin_headers):
    results = [('ER-524',119,148,9899,1480,Decimal('1.8512450281000003'),17,124,14354,Decimal('0.0011843388602480144907343'),Decimal('0.1031071478333565556639264'),Decimal('0.0086387069806325762853560'),Decimal('0.01148649'),2500),
               ('PK-452',26,53,780,346,Decimal(3827389.977),None,None,1647,None,Decimal(0.2100789313904068002428658),None,None,4625)]

    er524_premium_matrix_obj = FC_Premium_Matrix(results[0])
    er524_premium_matrix_obj.load_param()
    er524_premium_matrix_obj.run_algo()

    pk452_premium_matrix_obj = FC_Premium_Matrix(results[1])
    pk452_premium_matrix_obj.load_param()
    pk452_premium_matrix_obj.run_algo()

    premium_matrix_obj = FC_Premium_Matrix(results)
    premium_matrix_obj.load_param_matrix()
    premium_matrix_obj.run_matrix_algo()

    assert abs(er524_premium_matrix_obj.fc_participation_rate - Decimal(premium_matrix_obj.matrix[0][14])) < 0.0001
    assert abs(er524_premium_matrix_obj.PTCFactor - Decimal(premium_matrix_obj.matrix[0][12])) < 0.0001
    assert abs(er524_premium_matrix_obj.fc_exercise_rate - Decimal(premium_matrix_obj.matrix[0][9])) < 0.0001
    assert abs(er524_premium_matrix_obj.romr - Decimal(premium_matrix_obj.matrix[0][15])) < 0.0001
    assert abs(er524_premium_matrix_obj.sales - Decimal(premium_matrix_obj.matrix[0][16])) < 0.0001
    assert abs(er524_premium_matrix_obj.max_risk - Decimal(premium_matrix_obj.matrix[0][17])) < 0.0001
    assert abs(er524_premium_matrix_obj.ex_exercise_qty - Decimal(premium_matrix_obj.matrix[0][18])) < 0.0001
    assert abs(er524_premium_matrix_obj.tot_ex_charge - Decimal(premium_matrix_obj.matrix[0][19])) < 0.0001
    assert abs(er524_premium_matrix_obj.net_income - Decimal(premium_matrix_obj.matrix[0][20])) < 0.0001
    assert abs(er524_premium_matrix_obj.ex_premium_revenue - Decimal(premium_matrix_obj.matrix[0][21])) < 0.0001
    assert abs(er524_premium_matrix_obj.premium - Decimal(premium_matrix_obj.matrix[0][22])) < 0.0001

    assert abs(pk452_premium_matrix_obj.fc_participation_rate - Decimal(premium_matrix_obj.matrix[1][14])) < 0.0001
    assert abs(pk452_premium_matrix_obj.PTCFactor - Decimal(premium_matrix_obj.matrix[1][12])) < 0.0001
    assert abs(pk452_premium_matrix_obj.fc_exercise_rate - Decimal(premium_matrix_obj.matrix[1][9])) < 0.0001
    assert abs(pk452_premium_matrix_obj.romr - Decimal(premium_matrix_obj.matrix[1][15])) < 0.0001
    assert abs(pk452_premium_matrix_obj.sales - Decimal(premium_matrix_obj.matrix[1][16])) < 0.0001
    assert abs(pk452_premium_matrix_obj.max_risk - Decimal(premium_matrix_obj.matrix[1][17])) < 0.0001
    assert abs(pk452_premium_matrix_obj.ex_exercise_qty - Decimal(premium_matrix_obj.matrix[1][18])) < 0.0001
    assert abs(pk452_premium_matrix_obj.tot_ex_charge - Decimal(premium_matrix_obj.matrix[1][19])) < 0.0001
    assert abs(pk452_premium_matrix_obj.net_income - Decimal(premium_matrix_obj.matrix[1][20])) < 0.0001
    assert abs(pk452_premium_matrix_obj.ex_premium_revenue - Decimal(premium_matrix_obj.matrix[1][21])) < 0.0001
    assert abs(pk452_premium_matrix_obj.premium - Decimal(premium_matrix_obj.matrix[1][22])) < 0.0001
    assert abs(pk452_premium_matrix_obj.premium) >= 500 # Added by Mohib 18/05/2022


def test_single_fc_quote_calculation_pax(client, db, admin_headers, fcquote_collection_object, fcquote_object_pax):
    results = [('PK-203',119,148,9899,1480,Decimal('1.8512450281000003'),17,124,14354,Decimal('0.0011843388602480144907343'),Decimal('0.1031071478333565556639264'),Decimal('0.0086387069806325762853560'),Decimal('0.01148649'),2500)]
    # results = [('ER-524', 251, 352, 9773, 1456, Decimal('18057086.766000003'), 10, 113, 14184, Decimal('0.0007050197405527354765933'), Decimal('0.1026508742244782853919910'), Decimal('0.0079667230682459108855048'), Decimal('0.00686813'), 2500)]
    premium_matrix_obj = FC_Premium_Matrix(results[0])
    premium_matrix_obj.load_param(fcquote_object_pax)
    premium_matrix_obj.run_algo()

    assert premium_matrix_obj.fc_participation_rate == Decimal('0.008638706980632576285355998328')
    assert premium_matrix_obj.PTCFactor == Decimal('0.01148649')
    assert premium_matrix_obj.fc_exercise_rate == Decimal('0.0011843388602480144907343')
    assert premium_matrix_obj.romr == Decimal(0.05)
    assert premium_matrix_obj.sales == Decimal('1.278528633133621290232687753')
    assert premium_matrix_obj.max_risk == Decimal('3196.321582834053225581719382')
    assert premium_matrix_obj.ex_exercise_qty == Decimal('0.001514211144159924894381766310')
    assert premium_matrix_obj.tot_ex_charge == Decimal('3.785527860399812235954415775')
    assert premium_matrix_obj.net_income == Decimal('159.8160791417026701506605075')
    assert premium_matrix_obj.ex_premium_revenue == Decimal('163.6016070021024823866149233')
    assert premium_matrix_obj.premium >= 500*3 # fcquote_object_pax has set 2 adult pax + 1 child pax for this flight # Added by Mohib 18/05/2022


def test_multi_fc_quote_calculation_pax(client, db, admin_headers, fcquote_collection_schema_pax):
    results = [('ER-524',119,148,9899,1480,Decimal('1.8512450281000003'),17,124,14354,Decimal('0.0011843388602480144907343'),Decimal('0.1031071478333565556639264'),Decimal('0.0086387069806325762853560'),Decimal('0.01148649'),2500),
               ('PK-452',26,53,780,346,Decimal(3827389.977),None,None,1647,None,Decimal(0.2100789313904068002428658),None,None,4625)]

    er524_premium_matrix_obj = FC_Premium_Matrix(results[0])
    er524_premium_matrix_obj.load_param()
    er524_premium_matrix_obj.run_algo()

    pk452_premium_matrix_obj = FC_Premium_Matrix(results[1])
    pk452_premium_matrix_obj.load_param()
    pk452_premium_matrix_obj.run_algo()

    premium_matrix_obj = FC_Premium_Matrix(results)
    premium_matrix_obj.load_param_matrix(fcquote_collection_schema_pax)
    premium_matrix_obj.run_matrix_algo()

    assert abs(er524_premium_matrix_obj.fc_participation_rate - Decimal(premium_matrix_obj.matrix[0][14])) < 0.0001
    assert abs(er524_premium_matrix_obj.PTCFactor - Decimal(premium_matrix_obj.matrix[0][12])) < 0.0001
    assert abs(er524_premium_matrix_obj.fc_exercise_rate - Decimal(premium_matrix_obj.matrix[0][9])) < 0.0001
    assert abs(er524_premium_matrix_obj.romr - Decimal(premium_matrix_obj.matrix[0][15])) < 0.0001
    assert abs(er524_premium_matrix_obj.sales - Decimal(premium_matrix_obj.matrix[0][16])) < 0.0001
    assert abs(er524_premium_matrix_obj.max_risk - Decimal(premium_matrix_obj.matrix[0][17])) < 0.0001
    assert abs(er524_premium_matrix_obj.ex_exercise_qty - Decimal(premium_matrix_obj.matrix[0][18])) < 0.0001
    assert abs(er524_premium_matrix_obj.tot_ex_charge - Decimal(premium_matrix_obj.matrix[0][19])) < 0.0001
    assert abs(er524_premium_matrix_obj.net_income - Decimal(premium_matrix_obj.matrix[0][20])) < 0.0001
    assert abs(er524_premium_matrix_obj.ex_premium_revenue - Decimal(premium_matrix_obj.matrix[0][21])) < 0.0001
    assert abs(er524_premium_matrix_obj.premium * 2 - Decimal(premium_matrix_obj.matrix[0][22])) < 0.0001 # fcquote_collection_schema_pax has set 2 adult pax for this flight

    assert abs(pk452_premium_matrix_obj.fc_participation_rate - Decimal(premium_matrix_obj.matrix[1][14])) < 0.0001
    assert abs(pk452_premium_matrix_obj.PTCFactor - Decimal(premium_matrix_obj.matrix[1][12])) < 0.0001
    assert abs(pk452_premium_matrix_obj.fc_exercise_rate - Decimal(premium_matrix_obj.matrix[1][9])) < 0.0001
    assert abs(pk452_premium_matrix_obj.romr - Decimal(premium_matrix_obj.matrix[1][15])) < 0.0001
    assert abs(pk452_premium_matrix_obj.sales - Decimal(premium_matrix_obj.matrix[1][16])) < 0.0001
    assert abs(pk452_premium_matrix_obj.max_risk - Decimal(premium_matrix_obj.matrix[1][17])) < 0.0001
    assert abs(pk452_premium_matrix_obj.ex_exercise_qty - Decimal(premium_matrix_obj.matrix[1][18])) < 0.0001
    assert abs(pk452_premium_matrix_obj.tot_ex_charge - Decimal(premium_matrix_obj.matrix[1][19])) < 0.0001
    assert abs(pk452_premium_matrix_obj.net_income - Decimal(premium_matrix_obj.matrix[1][20])) < 0.0001
    assert abs(pk452_premium_matrix_obj.ex_premium_revenue - Decimal(premium_matrix_obj.matrix[1][21])) < 0.0001
    assert abs(pk452_premium_matrix_obj.premium*3 - Decimal(premium_matrix_obj.matrix[1][22])) < 0.0001 # fcquote_collection_schema_pax has set 1 adult pax + 2 child pax for this flight
    assert abs(pk452_premium_matrix_obj.premium) >= 500  # Added by Mohib 18/05/2022.


def test_multi_fc_quote_calculation_no_hist_pax(client, db, admin_headers, fcquote_collection_schema_pax):
    results = [('ER-524',None,None,9899,1480,Decimal('1.8512450281000003'),None,None,14354,None,Decimal('0.1031071478333565556639264'),None,None,2500),
               ('PK-452',26,53,780,346,Decimal(3827389.977),None,None,1647,None,Decimal(0.2100789313904068002428658),None,None,4625)]

    er524_premium_matrix_obj = FC_Premium_Matrix(results[0])
    er524_premium_matrix_obj.load_param()
    er524_premium_matrix_obj.run_algo()

    pk452_premium_matrix_obj = FC_Premium_Matrix(results[1])
    pk452_premium_matrix_obj.load_param()
    pk452_premium_matrix_obj.run_algo()

    premium_matrix_obj = FC_Premium_Matrix(results)
    premium_matrix_obj.load_param_matrix(fcquote_collection_schema_pax)
    premium_matrix_obj.run_matrix_algo()

    assert abs(er524_premium_matrix_obj.fc_participation_rate - Decimal(premium_matrix_obj.matrix[0][14])) < 0.0001
    assert abs(er524_premium_matrix_obj.PTCFactor - Decimal(premium_matrix_obj.matrix[0][12])) < 0.0001
    assert abs(er524_premium_matrix_obj.fc_exercise_rate - Decimal(premium_matrix_obj.matrix[0][9])) < 0.0001
    assert abs(er524_premium_matrix_obj.romr - Decimal(premium_matrix_obj.matrix[0][15])) < 0.0001
    # assert abs(er524_premium_matrix_obj.fc_sales - Decimal(premium_matrix_obj.matrix[0][16])) < 0.0001
    assert abs(er524_premium_matrix_obj.max_risk - Decimal(premium_matrix_obj.matrix[0][17])) < 0.0001
    assert abs(er524_premium_matrix_obj.ex_exercise_qty - Decimal(premium_matrix_obj.matrix[0][18])) < 0.0001
    assert abs(er524_premium_matrix_obj.tot_ex_charge - Decimal(premium_matrix_obj.matrix[0][19])) < 0.0001
    assert abs(er524_premium_matrix_obj.net_income - Decimal(premium_matrix_obj.matrix[0][20])) < 0.0001
    assert abs(er524_premium_matrix_obj.ex_premium_revenue - Decimal(premium_matrix_obj.matrix[0][21])) < 0.0001
    assert abs(er524_premium_matrix_obj.premium * 2 - Decimal(premium_matrix_obj.matrix[0][22])) < 0.0001 # fcquote_collection_schema_pax has set 2 adult pax for this flight

    assert abs(pk452_premium_matrix_obj.fc_participation_rate - Decimal(premium_matrix_obj.matrix[1][14])) < 0.0001
    assert abs(pk452_premium_matrix_obj.PTCFactor - Decimal(premium_matrix_obj.matrix[1][12])) < 0.0001
    assert abs(pk452_premium_matrix_obj.fc_exercise_rate - Decimal(premium_matrix_obj.matrix[1][9])) < 0.0001
    assert abs(pk452_premium_matrix_obj.romr - Decimal(premium_matrix_obj.matrix[1][15])) < 0.0001
    assert abs(pk452_premium_matrix_obj.sales - Decimal(premium_matrix_obj.matrix[1][16])) < 0.0001
    assert abs(pk452_premium_matrix_obj.max_risk - Decimal(premium_matrix_obj.matrix[1][17])) < 0.0001
    assert abs(pk452_premium_matrix_obj.ex_exercise_qty - Decimal(premium_matrix_obj.matrix[1][18])) < 0.0001
    assert abs(pk452_premium_matrix_obj.tot_ex_charge - Decimal(premium_matrix_obj.matrix[1][19])) < 0.0001
    assert abs(pk452_premium_matrix_obj.net_income - Decimal(premium_matrix_obj.matrix[1][20])) < 0.0001
    assert abs(pk452_premium_matrix_obj.ex_premium_revenue - Decimal(premium_matrix_obj.matrix[1][21])) < 0.0001
    assert abs(pk452_premium_matrix_obj.premium*3 - Decimal(premium_matrix_obj.matrix[1][22])) < 0.0001 # fcquote_collection_schema_pax has set 1 adult pax + 2 child pax for this flight
    assert abs(pk452_premium_matrix_obj.premium) >= 500  # Added by Mohib 18/05/2022.


def test_multi_fc_quote_calculation_pax_ceiling(client, db, admin_headers, fcquote_collection_schema_pax):
    results = [('ER-524',119,148,9899,1480,Decimal('1.8512450281000003'),17,124,14354,Decimal('0.0011843388602480144907343'),Decimal('0.1031071478333565556639264'),Decimal('0.0086387069806325762853560'),Decimal('0.01148649'),1000),
               ('PK-452',26,53,780,346,Decimal(3827389.977),None,None,1647,None,Decimal(0.2100789313904068002428658),None,None,1000)]

    er524_premium_matrix_obj = FC_Premium_Matrix(results[0])
    er524_premium_matrix_obj.load_param()
    er524_premium_matrix_obj.run_algo()

    pk452_premium_matrix_obj = FC_Premium_Matrix(results[1])
    pk452_premium_matrix_obj.load_param()
    pk452_premium_matrix_obj.run_algo()

    premium_matrix_obj = FC_Premium_Matrix(results)
    premium_matrix_obj.load_param_matrix()
    premium_matrix_obj.run_matrix_algo()

    premium_matrix_obj_pax = FC_Premium_Matrix(results)
    premium_matrix_obj_pax.load_param_matrix(fcquote_collection_schema_pax)
    premium_matrix_obj_pax.run_matrix_algo()

    comp_arr = premium_matrix_obj.matrix[:,22] < premium_matrix_obj.matrix[:,13]

    assert abs(er524_premium_matrix_obj.premium) < abs(er524_premium_matrix_obj.charge)
    assert abs(pk452_premium_matrix_obj.premium) < abs(pk452_premium_matrix_obj.charge)
    assert comp_arr.all() == True

    assert abs(er524_premium_matrix_obj.premium < Decimal(premium_matrix_obj.matrix[0][13]))
    assert abs(pk452_premium_matrix_obj.premium < Decimal(premium_matrix_obj.matrix[1][13]))
