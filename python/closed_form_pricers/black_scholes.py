from parameter_files import daycount_convention
from parameter_files.marketData import *
from parameter_files.tradeParameters import vanillaEquityOption
from parameter_files.daycount_convention import *
import numpy as np
from scipy.stats import norm
from parameter_files.vol_fetcher import vol_fetcher


def black_scholes(md: market_data, pd: vanillaEquityOption, vo: vol_fetcher):
    if pd.is_call == True:
        payoff_type = 1
    else:
        payoff_type = -1

    maturity = daycount(md.val_date, pd.maturity, pd.dayCountConvention)
    volatility = vo.retrieve_vol(md.spot, maturity)

    d1 = (np.log(md.spot / pd.strike) + (md.interest_rate - md.divYield + 0.5 * np.pow(volatility, 2)) * maturity)/ (volatility * np.sqrt(maturity))
    d2 = d1 - volatility * np.sqrt(maturity)

    option_value = payoff_type * md.spot * np.exp(-md.div_yield*maturity)*norm.cdf(payoff_type * d1) - payoff_type*pd.strike*np.exp(- md.interest_rate * maturity) *norm.cdf(payoff_type * d2)

    delta = payoff_type * np.exp(-md.div_yield*maturity)*norm.cdf(payoff_type * d1)
    vega = md.spot * np.exp(-md.div_yield*maturity)*norm.pdf(d1) * np.sqrt(maturity) / 100
    gamma = (np.exp(-md.div_yield*maturity)*norm.pdf(d1)) / (volatility * np.sqrt(maturity)) / 100

    theta = (
    -(md.spot * np.exp(-md.div_yield * maturity) * norm.pdf(d1) * volatility) / (2 * np.sqrt(maturity))
    - payoff_type * md.interest_rate * pd.strike
      * np.exp(-md.interest_rate * maturity) * norm.cdf(payoff_type * d2)
    + payoff_type * md.div_yield * md.spot
      * np.exp(-md.div_yield * maturity) * norm.cdf(payoff_type * d1)) / 365
    log_file_output = {
        "option_value": option_value,
        "d1": d1,
        "d2": d2,
        "Probability of ITM": norm.cdf(payoff_type * d2),
        "Delta": delta,
        "Vega %": vega,
        "Gamma per unit": gamma,
        "Theta per day" : theta,
        "volatility": volatility
    }
    return log_file_output
