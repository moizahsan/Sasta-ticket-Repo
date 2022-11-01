import json

import sqlalchemy as db
from flask import abort

from dsapi.models import Premium_Matrix, QuoteModel, FC_Premium_Matrix, DC_Premium_Matrix
from dsapi.settings.config import DREMIO_USERNAME, DREMIO_PASSWORD


def calculate_premium(quote_obj):
    results = get_premium_matrix(quote_obj)
    # trailing_pax_results = get_trailing_pax_matrix(fcquote_obj)

    if len(results) == 0:
        abort(404)

    if quote_obj.quote_type == 'fc':
        premium_matrix_obj = FC_Premium_Matrix(results[0])

    if quote_obj.quote_type == 'dc':
        premium_matrix_obj = DC_Premium_Matrix(results[0])

    premium_matrix_obj.load_param(quote_obj)
    premium_matrix_obj.run_algo()
    quote_obj = save_premium(quote_obj, premium_matrix_obj)
    return quote_obj


def get_premium_matrix(quote_obj):

    if quote_obj.quote_type == 'fc':
        engine = db.create_engine(
            f"dremio://{DREMIO_USERNAME}:{DREMIO_PASSWORD}@dremio.sastaticket.pk:31010/dremio;SSL=0"
        )
        connection = engine.connect()
        sql = (
            """SELECT * FROM "Fintech_API"."vw_premium_matrix" A where A.flight_number= '%s'"""
            % quote_obj.flight_number
        )
        results = engine.execute(sql)
        results_list = results.all()

    if quote_obj.quote_type == 'dc':
        engine = db.create_engine(
            f"dremio://{DREMIO_USERNAME}:{DREMIO_PASSWORD}@dremio.sastaticket.pk:31010/dremio;SSL=0"
        )
        connection = engine.connect()
        sql = (
            """SELECT * FROM "Fintech_API"."vw_premium_matrix_dc" A where A.flight_number= '%s'"""
            % quote_obj.flight_number
        )
        results = engine.execute(sql)
        results_list = results.all()

    print('got results')
    return results_list


def get_trailing_pax_matrix(fcquote_obj):
    engine = db.create_engine(
        f"dremio://{DREMIO_USERNAME}:{DREMIO_PASSWORD}@dremio.sastaticket.pk:31010/dremio;SSL=0"
    )
    connection = engine.connect()
    sql = (
        """SELECT flight_number, rel_week_no, CnclFCPaxQtyByWeek, FCPaxQtyByWeek, fc_exercise_rate FROM "Fintech_API"."vw_weekly_trailing_fc" A where A.flight_number= '%s' and rel_week_no < 1 order by rel_week_no DESC"""
        % fcquote_obj.flight_number
    )
    results = engine.execute(sql)
    results_list = results.all()

    return results_list

def get_premium_matrix_sql(sql):
    engine = db.create_engine(
        f"dremio://{DREMIO_USERNAME}:{DREMIO_PASSWORD}@dremio.sastaticket.pk:31010/dremio;SSL=0"
    )
    connection = engine.connect()
    results = engine.execute(sql)
    results_list = results.all()

    return results_list


def create_dremio_query(quote_type, flight_numbers):
    if quote_type == 'fc':
        sql = """SELECT * FROM "Fintech_API"."vw_premium_matrix" A where A.flight_number in ("""

        if len(flight_numbers) > 1:
            for fn in flight_numbers:
                sql += """'%s',""" % fn

            sql = sql[:-1]
            sql += """)"""
        else:
            sql += """'%s')""" % flight_numbers[0]
        return sql

    if quote_type == 'dc':
        sql = """SELECT * FROM "Fintech_API"."vw_premium_matrix_dc" A where A.flight_number in ("""

        if len(flight_numbers) > 1:
            for fn in flight_numbers:
                sql += """'%s',""" % fn

            sql = sql[:-1]
            sql += """)"""
        else:
            sql += """'%s')""" % flight_numbers[0]
        return sql


def save_premium(quote_obj, premium_matrix_obj):
    if quote_obj.quote_type == 'fc':
        quote_obj.premium = float(premium_matrix_obj.premium)
        quote_obj.model_param = json.dumps(
            {
                "trailing_avg_order_qty": int(premium_matrix_obj.trailing_avg_order_qty),
                "trail_weekly_tot_pax_count": int(
                    premium_matrix_obj.trail_weekly_tot_pax_count
                ),
                "order_qty": float(premium_matrix_obj.order_qty),
                "cncl_pax_count": float(premium_matrix_obj.cncl_pax_count),
                "cncl_amt": float(premium_matrix_obj.cncl_amt),
                "cncl_fc_pax_count": int(premium_matrix_obj.cncl_fc_pax_count),
                "fc_pax_count": int(premium_matrix_obj.fc_pax_count),
                "tot_pax_count": int(premium_matrix_obj.tot_pax_count),
                "fc_exercise_rate": float(premium_matrix_obj.fc_exercise_rate),
                "gen_cncl_rate": float(premium_matrix_obj.gen_cncl_rate),
                "participation_rate": float(premium_matrix_obj.participation_rate),
                "PTCFactor": float(premium_matrix_obj.PTCFactor),
                "cncl_charge": float(premium_matrix_obj.charge),
                "fc_participation_rate": float(premium_matrix_obj.fc_participation_rate),
                "romr": float(premium_matrix_obj.romr),
                "max_risk": float(premium_matrix_obj.max_risk),
                "fc_sales": float(premium_matrix_obj.sales),
                "ex_exercise_qty": float(premium_matrix_obj.ex_exercise_qty),
                "tot_ex_cncl_charge": float(premium_matrix_obj.tot_ex_charge),
                "net_income": float(premium_matrix_obj.net_income),
                "ex_premium_revenue": float(premium_matrix_obj.ex_premium_revenue),
            }
        )

    if quote_obj.quote_type == 'dc':
        quote_obj.premium = float(premium_matrix_obj.premium)
        quote_obj.model_param = json.dumps(
            {
                "trailing_avg_order_qty": int(premium_matrix_obj.trailing_avg_order_qty),
                "trail_weekly_tot_pax_count": int(
                    premium_matrix_obj.trail_weekly_tot_pax_count
                ),
                "order_qty": float(premium_matrix_obj.order_qty),
                "chnge_pax_count": float(premium_matrix_obj.chnge_pax_count),
                "chnge_amt": float(premium_matrix_obj.chnge_amt),
                "chnge_dc_pax_count": int(premium_matrix_obj.chnge_dc_pax_count),
                "dc_pax_count": int(premium_matrix_obj.dc_pax_count),
                "tot_pax_count": int(premium_matrix_obj.tot_pax_count),
                "dc_exercise_rate": float(premium_matrix_obj.dc_exercise_rate),
                "gen_chnge_rate": float(premium_matrix_obj.gen_chnge_rate),
                "participation_rate": float(premium_matrix_obj.participation_rate),
                "chnge_charge": float(premium_matrix_obj.charge),
                "dc_participation_rate": float(premium_matrix_obj.dc_participation_rate),
                "romr": float(premium_matrix_obj.romr),
                "max_risk": float(premium_matrix_obj.max_risk),
                "dc_sales": float(premium_matrix_obj.sales),
                "ex_exercise_qty": float(premium_matrix_obj.ex_exercise_qty),
                "tot_ex_cncl_charge": float(premium_matrix_obj.tot_ex_charge),
                "net_income": float(premium_matrix_obj.net_income),
                "ex_premium_revenue": float(premium_matrix_obj.ex_premium_revenue),
            }
        )

    quote_obj.save_to_db()

    return quote_obj


def save_premium_matrix(quote_collection_obj, premium_matrix_obj, quote_collection_data):
    """
    assumption:
    One flight number will only appear once per call
    
    """
    quote_collection_obj.save_to_db()

    for idx, premium_matrix_obj in enumerate(premium_matrix_obj.matrix):
        pruned_quotes = list(filter(lambda x:x["flight_number"] == premium_matrix_obj[0], quote_collection_data['fcquotes']))

        for temp_idx, quote_req in enumerate(quote_collection_data['fcquotes']):
            if quote_req['flight_number'] == premium_matrix_obj[0]:
                param_idx = temp_idx
                break

        fcquote_obj = QuoteModel(
            collection_id=quote_collection_obj.id,
            flight_number=premium_matrix_obj[0],
            quote_type="fc",
            premium=premium_matrix_obj[22],
            param=pruned_quotes[0].get('param', None),
            model_param=json.dumps(
                {
                    "trailing_avg_order_qty": int(premium_matrix_obj[1]),
                    "trail_weekly_tot_pax_count": int(premium_matrix_obj[2]),
                    "order_qty": float(premium_matrix_obj[3]),
                    "cncl_pax_count": float(premium_matrix_obj[4]),
                    "cncl_amt": float(premium_matrix_obj[5]),
                    "cncl_fc_pax_count": int(premium_matrix_obj[6]),
                    "fc_pax_count": int(premium_matrix_obj[7]),
                    "tot_pax_count": int(premium_matrix_obj[8]),
                    "fc_exercise_rate": float(premium_matrix_obj[9]),
                    "gen_cncl_rate": float(premium_matrix_obj[10]),
                    "participation_rate": float(premium_matrix_obj[11]),
                    "PTCFactor": float(premium_matrix_obj[12]),
                    "cncl_charge": float(premium_matrix_obj[13]),
                    "fc_participation_rate": float(premium_matrix_obj[14]),
                    "romr": float(premium_matrix_obj[15]),
                    "max_risk": float(premium_matrix_obj[17]),
                    "fc_sales": float(premium_matrix_obj[16]),
                    "ex_exercise_qty": float(premium_matrix_obj[18]),
                    "tot_ex_cncl_charge": float(premium_matrix_obj[19]),
                    "net_income": float(premium_matrix_obj[20]),
                    "ex_premium_revenue": float(premium_matrix_obj[21]),
                }
            ),
        )
        fcquote_obj.save_to_db()
        quote_collection_obj.fcquotes.append(fcquote_obj)
    quote_collection_obj.save_to_db()
    return quote_collection_obj


def calculate_multi_premiums(quote_collection_obj, quote_collection_data, api_version=1.1):
    sql = create_dremio_query(quote_collection_obj.quote_type,
        [x["flight_number"] for x in quote_collection_data["fcquotes"]]
    )

    results = get_premium_matrix_sql(sql)

    if quote_collection_obj.quote_type =='fc':
        premium_matrix_obj = FC_Premium_Matrix(results)

    if quote_collection_obj.quote_type =='dc':
        premium_matrix_obj = DC_Premium_Matrix(results)

    if len(results) == 0:
        abort(404)

    if api_version == 1.1:
        premium_matrix_obj.load_param_matrix(quote_collection_data)
    else:
        premium_matrix_obj.load_param_matrix()

    premium_matrix_obj.run_matrix_algo()

    quote_collection_obj = save_premium_matrix(quote_collection_obj, premium_matrix_obj, quote_collection_data)
    return quote_collection_obj
