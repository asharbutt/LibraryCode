from scipy.cluster.hierarchy import average

from parameter_files import marketData, tradeParameters
import parameter_files.marketData as market_data
from parameter_files.tradeParameters import *
import numpy as np
from parameter_files.daycount_convention import *
from scipy.stats import norm
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Optional
import closed_form_pricers.black_scholes as bs
import closed_form_pricers.digitals as dg
import sde_processes as sde

def simple_normal_random_generator(random_number_matrix):
    return norm.rvs(size=(random_number_matrix.shape[0], random_number_matrix.shape[1]))

class MonteCarloEngine:
    def __init__(self, num_steps, num_paths, data: market_data.market_data, params: Trade):
        self.num_steps = num_steps
        self.num_paths = num_paths
        self.data = data
        self.params = params
        self.equity_process = "gbm"

    def price_european_option(self):
        price = self.generate_paths()
        return np.average(price)

    def generate_paths(self):
        # first generate the random numbers needed. If we are running just a fixed volatility, or local volatility, then we only need a single set of random numbers for one Brownian Motion,  if Heston, then we need 2 sets of random numbers
        random_numbers = np.zeros((self.num_paths//2, self.num_steps+1))
        random_numbers = simple_normal_random_generator(random_numbers)
        maturity = daycount(self.data.valDate, self.params.maturity, self.params.dayCountConvention)
        if self.params.product_type == "vanilla_equity_option" or "digital_option":
            if self.equity_process == "gbm":
                paths = sde.geometric_brownian_motion(random_numbers, self.data.interestRate, self.data.volatility, self.data.spot, maturity/self.num_steps)
                return self.params.payoff(paths[:,-1])*np.exp(-self.data.interestRate*maturity)

def main():
    market_data_object = market_data.market_data(spot=100, vol_type="fixed_vol", interestRate=0.05, divYield=0.0,
                                        valDate="26/09/2026", volatility=0.3)
    trade1_parameters = vanillaEquityOption(tradeID="trade1", is_call=True, notional=100, strike=100,
                                                     maturity="26/09/2027", dayCountConvention="A360")
    trade2_parameters = digitalOption(tradeID="trade1", is_call=True, notional=100, strike=100,
                                            maturity="26/09/2027", dayCountConvention="A360", fixed_payout=10)
    a = MonteCarloEngine(1000, 20000, market_data_object, trade2_parameters)
    print(a.price_european_option())
    print(dg.digital_option_closed_form(market_data_object, trade2_parameters))

main()
