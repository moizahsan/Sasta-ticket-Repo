import numpy as np

from decimal import Decimal


class Premium_Matrix(object):
    '''
    Base class which holds common functions
    '''

    def __init__(self, premium_result_tuple):
        self.result_tuple = premium_result_tuple

    def load_param(self, quote_obj=None):
        if quote_obj is not None and getattr(quote_obj,'param'):
            self.adult_pax = Decimal(quote_obj.param['adult_pax'])
            self.child_pax = Decimal(quote_obj.param['child_pax'])
        else:
            self.adult_pax = Decimal(1)
            self.child_pax = Decimal(0)


    def calculate_net_income(self):
        self.net_income = self.max_risk * self.romr

    def calculate_pax(self):
        self.premium = self.premium * (self.adult_pax + self.child_pax)
        return self.premium

    def set_guards(self):
        self.premium = self.premium * Decimal(0.8) #added by Mohib on 19th Sept 2022

        if self.premium > self.charge:
            self.premium = self.charge

        if self.premium < 500:
            self.premium = 500

        return self.premium


    def assign_values_matrix(self):
        self.matrix = np.asarray(self.result_tuple)
        self.matrix = self.matrix[self.matrix[:,0].argsort()]
        self.matrix[self.matrix==None]= 0.0
        self.matrix=np.c_[ self.matrix, np.ones(len(self.result_tuple)) * self.matrix[:,7] / self.matrix[:,8] ] # fc_participation_rate


    def load_param_matrix(self, quote_collection_data=None):
        """
        - if no collectionn data assume 1 pax
        - if collection data == sql results then load all
        - if collection data > sql then prune data

        find all flight numbers that are relevant. Pop from result_tuple
        - collection data <= sql is NOT possible

        Assumptions: SQL result will always have specified structure
        """

        if quote_collection_data is not None:
            pruned_quotes_temp = list(set([y['flight_number'] for y in quote_collection_data['fcquotes']]).intersection([z[0] for z in self.result_tuple]))

            for flgt_number in pruned_quotes_temp:
                pruned_quotes = list(filter(lambda x:x["flight_number"] in pruned_quotes_temp, quote_collection_data['fcquotes']))

            if len(quote_collection_data['fcquotes']) > len(self.result_tuple):

                self.param = np.asarray([(x['flight_number'],x['param']['adult_pax'],x['param']['child_pax']) for x in pruned_quotes])
                self.param[:,1] = self.param[:,1].astype(float)
                self.param[:,2] = self.param[:,2].astype(float)

            else:
                self.param = np.asarray([(x['flight_number'],x['param']['adult_pax'],x['param']['child_pax']) for x in quote_collection_data['fcquotes']])
                self.param[:,1] = self.param[:,1].astype(float)
                self.param[:,2] = self.param[:,2].astype(float)
                self.param = self.param[self.param[:,0].argsort()]
        else:
            self.param = np.zeros((len(self.result_tuple),3))
            self.param[:,0] = 0
            self.param[:,1] = float(1) # default 1 adult
            self.param[:,2] = float(0) # default 0 children

    def calculate_max_risk(self):
        self.max_risk = self.sales * self.charge


    def calculate_tot_expected_charges(self):
        self.tot_ex_charge = self.ex_exercise_qty * self.charge


    def calculate_expected_premium_revenue(self):
        self.ex_premium_revenue = self.net_income + self.tot_ex_charge


    def calculate_premium(self):
        if self.sales != 0:
            self.premium = self.ex_premium_revenue / self.sales
        else:
            self.premium = 500
        return self.premium


    def run_algo(self):
        self.assign_values()
        self.set_up_assumptions()
        self.calculate_sales()
        self.calculate_max_risk()
        self.calculate_expected_exercise_qty()
        self.calculate_tot_expected_charges()
        self.calculate_net_income()
        self.calculate_expected_premium_revenue()
        self.calculate_premium()
        self.set_guards()
        return self.calculate_pax()


    def set_up_assumptions_matrix(self):
        '''
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate)
        len = 15

        Matrix at end
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate, romr)
        len = 16
        '''
        self.matrix[:,14][self.matrix[:,14] == 0] = 0.1 # fc participation rate
        self.matrix[:,12][self.matrix[:,12] == 0] = 3.0 # PTC Factor

        self.matrix[:,10] = self.matrix[:,10].astype(float) # gen_cncl_rate
        self.matrix[:,12] = self.matrix[:,12].astype(float) # PTC Factor

        for row in np.where(self.matrix[:,9] == 0)[0]: # fc_exercise_rate
            self.matrix[row,9]= (self.matrix[row,10]*self.matrix[row,12]) # fc_exercise_rate
        self.matrix=np.c_[ self.matrix, np.ones(len(self.result_tuple)) * 0.05 ] # romr

    def calculate_sales_matrix(self):
        '''
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate, romr)
        len = 16

        Matrix at end
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate, romr, fc_sales)
        len = 17
        '''
        self.matrix[:,3] = self.matrix[:,3].astype(float) # trail_weekly_tot_pax_count
        self.matrix[:,14] = self.matrix[:,14].astype(float) # fc_participation_rate / dc participation rate
        self.matrix=np.c_[ self.matrix, np.ones(len(self.result_tuple))*self.matrix[:,2] * self.matrix[:,14] ]

    def calculate_max_risk_matrix(self):
        '''
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate, romr, fc_sales)
        len = 17

        Matrix at end
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate, romr, fc_sales, max_risk)
        len = 18
        '''
        self.matrix[:,16] = self.matrix[:,16].astype(float) # fc sales
        self.matrix[:,13] = self.matrix[:,13].astype(float) # cncl charges
        self.matrix=np.c_[ self.matrix, np.ones(len(self.result_tuple))*self.matrix[:,13]*self.matrix[:,16] ]

    def calculate_expected_exercise_qty_matrix(self):
        '''
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate, romr, fc_sales, max_risk)
        len = 18

        Matrix at end
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate, romr, fc_sales, max_risk, ex_exercise_qty)
        len = 19
        '''
        self.matrix[:,9] = self.matrix[:,9].astype(float) # fc_exercise_rate
        self.matrix=np.c_[ self.matrix, np.ones(len(self.result_tuple))*self.matrix[:,16]*self.matrix[:,9] ] # fc_sales * fc_exercise_rate

    def calculate_tot_expected_charges_matrix(self):
        '''
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate, romr, fc_sales, max_risk, ex_exercise_qty)
        len = 19

        Matrix at end
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate, romr, fc_sales, max_risk, ex_exercise_qty, tot_ex_cncl_charge)
        len = 20
        '''
        self.matrix=np.c_[ self.matrix, np.ones(len(self.result_tuple))*self.matrix[:,18]*self.matrix[:,13] ] # ex_exercise_qty * cncl_charge

    def calculate_net_income_matrix(self):
        '''
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate, romr, fc_sales, max_risk, ex_exercise_qty, tot_ex_cncl_charge)
        len = 20

        Matrix at end
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate, romr, fc_sales, max_risk, ex_exercise_qty, tot_ex_cncl_charge, net_income)
        len = 21
        '''
        self.matrix=np.c_[ self.matrix, np.ones(len(self.result_tuple))*self.matrix[:,17]*self.matrix[:,15] ]  # max_risk * romr

    def calculate_expected_premium_revenue_matrix(self):
        '''
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate, romr, fc_sales, max_risk, ex_exercise_qty, tot_ex_cncl_charge, net_income)
        len = 21

        Matrix at end
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate, romr, fc_sales, max_risk, ex_exercise_qty, tot_ex_cncl_charge, net_income, ex_premium_revenue)
        len = 22
        '''
        self.matrix=np.c_[ self.matrix, np.ones(len(self.result_tuple))*(self.matrix[:,20] + self.matrix[:,19]) ] # net_income + tot_ex_cncl_charge


    def calculate_premium_matrix(self):
        '''
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate, romr, fc_sales, max_risk, ex_exercise_qty, tot_ex_cncl_charge, net_income)
        len = 22

        Matrix at end
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, cncl_pax_count, cncl_amt, cncl_fc_pax_count, fc_pax_count, tot_pax_count, fc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, cncl_charge, fc_participation_rate, romr, fc_sales, max_risk, ex_exercise_qty, tot_ex_cncl_charge, net_income, ex_premium_revenue, premium)
        len = 23
        '''
        self.matrix[:,16][self.matrix[:,16] == None] = 1
        self.matrix[:,16][self.matrix[:,16] == 0] = 1
        self.matrix=np.c_[ self.matrix, np.ones(len(self.result_tuple))*self.matrix[:,21]/self.matrix[:,16] ]

    def calculate_pax_matrix(self):
        self.matrix[:,22] = self.matrix[:,22] * (self.param[:,1].astype(float) + self.param[:,2].astype(float))

    def set_guards_matrix(self):
        self.matrix[:,22] = self.matrix[:,22] * (np.ones(len(self.result_tuple)) * 0.8) #added by Mohib on 19th Sept 2022
        self.matrix[:,22][self.matrix[:,22] < 500] = 500
        self.matrix[:,22] = np.fmin(self.matrix[:,22], self.matrix[:,13])

    def run_matrix_algo(self):
        self.assign_values_matrix()
        self.set_up_assumptions_matrix()
        self.calculate_sales_matrix()
        self.calculate_max_risk_matrix()
        self.calculate_expected_exercise_qty_matrix()
        self.calculate_tot_expected_charges_matrix()
        self.calculate_net_income_matrix()
        self.calculate_expected_premium_revenue_matrix()
        self.calculate_premium_matrix()
        self.set_guards_matrix()
        return self.calculate_pax_matrix()


class FC_Premium_Matrix(Premium_Matrix):
    """
    Algo limitations:
    - using overall time period av vs 3 period
    - using max cancellation charges instead of weighted average
    - using fixed ROMR
    - assumes child_pax and adult_pax cancellation charges are the same
    """

    def assign_values(self):
        self.name = self.result_tuple[0]
        self.trailing_avg_order_qty = Decimal(self.result_tuple[1]) if self.result_tuple[1] is not None else Decimal(0)
        self.trail_weekly_tot_pax_count = Decimal(self.result_tuple[2]) if self.result_tuple[2] is not None else Decimal(0)
        self.order_qty = Decimal(self.result_tuple[3]) if self.result_tuple[3] is not None else Decimal(0)
        self.cncl_pax_count = Decimal(self.result_tuple[4]) if self.result_tuple[4] is not None else Decimal(0)
        self.cncl_amt = Decimal(self.result_tuple[5]) if self.result_tuple[5] is not None else Decimal(0)
        self.cncl_fc_pax_count = Decimal(self.result_tuple[6]) if self.result_tuple[6] is not None else Decimal(0)
        self.fc_pax_count = Decimal(self.result_tuple[7]) if self.result_tuple[7] is not None else Decimal(0)
        self.tot_pax_count = Decimal(self.result_tuple[8]) if self.result_tuple[8] is not None else Decimal(0)
        self.fc_exercise_rate = Decimal(self.result_tuple[9]) if self.result_tuple[9] is not None else Decimal(0)
        self.gen_cncl_rate = Decimal(self.result_tuple[10]) if self.result_tuple[10] is not None else Decimal(0)
        self.participation_rate = Decimal(self.result_tuple[11]) if self.result_tuple[11] is not None else Decimal(0)
        self.PTCFactor = Decimal(self.result_tuple[12]) if self.result_tuple[12] is not None else Decimal(0)
        self.charge = Decimal(self.result_tuple[13]) if self.result_tuple[13] is not None else Decimal(0)
        self.fc_participation_rate = (self.fc_pax_count / self.tot_pax_count)


    def set_up_assumptions(self):
        if self.fc_participation_rate.is_zero():
            self.fc_participation_rate = Decimal(0.1)

        if self.PTCFactor.is_zero():
            self.PTCFactor = Decimal(3)

        if self.fc_exercise_rate.is_zero():
            self.fc_exercise_rate = self.gen_cncl_rate * self.PTCFactor

        self.romr = Decimal(0.05)


    def calculate_sales(self):
        self.sales = self.trail_weekly_tot_pax_count * self.fc_participation_rate


    def calculate_expected_exercise_qty(self):
        self.ex_exercise_qty = self.sales * self.fc_exercise_rate


class DC_Premium_Matrix(Premium_Matrix):
    """
    Algo limitations:
    - using overall time period av vs 3 period
    - using max cancellation charges instead of weighted average
    - using fixed ROMR
    - assumes child_pax and adult_pax cancellation charges are the same
    """
    def assign_values(self):
        self.name = self.result_tuple[0]
        self.trailing_avg_order_qty = Decimal(self.result_tuple[1]) if self.result_tuple[1] is not None else Decimal(0)
        self.trail_weekly_tot_pax_count = Decimal(self.result_tuple[2]) if self.result_tuple[2] is not None else Decimal(0)
        self.order_qty = Decimal(self.result_tuple[3]) if self.result_tuple[3] is not None else Decimal(0)
        self.chnge_pax_count = Decimal(self.result_tuple[4]) if self.result_tuple[4] is not None else Decimal(0)
        self.chnge_amt = Decimal(self.result_tuple[5]) if self.result_tuple[5] is not None else Decimal(0)
        self.chnge_dc_pax_count = Decimal(self.result_tuple[6]) if self.result_tuple[6] is not None else Decimal(0)
        self.dc_pax_count = Decimal(self.result_tuple[7]) if self.result_tuple[7] is not None else Decimal(0)
        self.tot_pax_count = Decimal(self.result_tuple[8]) if self.result_tuple[8] is not None else Decimal(0)
        self.dc_exercise_rate = Decimal(self.result_tuple[9]) if self.result_tuple[9] is not None else Decimal(0)
        self.gen_chnge_rate = Decimal(self.result_tuple[10]) if self.result_tuple[10] is not None else Decimal(0)
        self.participation_rate = Decimal(self.result_tuple[11]) if self.result_tuple[11] is not None else Decimal(0)
        self.PTCFactor = Decimal(self.result_tuple[12]) if self.result_tuple[12] is not None else Decimal(0) #IS NA
        self.charge = Decimal(self.result_tuple[13]) if self.result_tuple[13] is not None else Decimal(0)
        self.dc_participation_rate = (self.dc_pax_count / self.tot_pax_count)


    def set_up_assumptions(self):
        if self.dc_participation_rate.is_zero():
            self.dc_participation_rate = Decimal(0.1)

        if self.dc_exercise_rate.is_zero():
            self.dc_exercise_rate = Decimal(0.1)

        self.romr = Decimal(0.05)


    def calculate_sales(self):
        self.sales = self.trail_weekly_tot_pax_count * self.dc_participation_rate


    def calculate_expected_exercise_qty(self):
        self.ex_exercise_qty = self.sales * self.dc_exercise_rate


    def set_up_assumptions_matrix(self):
        '''
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, chnge_pax_count, chnge_amt, chnge_dc_pax_count, dc_pax_count, tot_pax_count, dc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, chnge_charge, dc_participation_rate)
        len = 15

        Matrix at end
        Matrix at start  (flight, trailing_avg_order_qty, trail_weekly_tot_pax_count, order_qty, chnge_pax_count, chnge_amt, chnge_dc_pax_count, dc_pax_count, tot_pax_count, dc_exercise_rate, gen_cncl_rate, participation_rate, PTCFactor, chnge_charge, dc_participation_rate, romr)
        len = 16
        '''
        self.matrix[:,14][self.matrix[:,14] == 0] = 0.1 # dc participation rate
        self.matrix[:,9][self.matrix[:,9] == 0] = 0.1 # dc exercise rate
        self.matrix[:,12][self.matrix[:,12] == 0] = 0.0 # PTC Factor = NA

        self.matrix[:,10] = self.matrix[:,10].astype(float) # gen_cncl_rate
        self.matrix[:,12] = self.matrix[:,12].astype(float) # PTC Factor = NA

        self.matrix=np.c_[ self.matrix, np.ones(len(self.result_tuple)) * 0.05 ] # romr

    def set_guards_matrix(self):
        self.matrix[:,22][self.matrix[:,22] < 500] = 500
        self.matrix[:,22] = np.fmin(self.matrix[:,22], self.matrix[:,13])


    def set_guards(self):
        if self.premium > self.charge:
            self.premium = self.charge

        if self.premium < 500:
            self.premium = 500

        return self.premium
