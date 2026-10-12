from parameter_files import daycount_convention
from parameter_files.marketData import *
from parameter_files.tradeParameters import *
from parameter_files.daycount_convention import *
import numpy as np
from scipy.stats import norm
from parameter_files.vol_fetcher import vol_fetcher

def digital_cash_or_nothing(md: market_data, pd: digitalOption, vo: vol_fetcher):
    if pd.is_call == True:
        payoff_type = 1
    else:
        payoff_type = -1
    maturity = daycount(md.val_date, pd.maturity, pd.dayCountConvention)
    volatility = vo.retrieve_vol(md.spot, maturity)

    d1 = (np.log(md.spot / pd.strike) + (md.interest_rate - md.div_yield + 0.5 * np.pow(volatility, 2)) * maturity)/ (volatility * np.sqrt(maturity))
    d2 = d1 - volatility*np.sqrt(maturity)
    delta_digital = payoff_type*pd.fixed_payout*np.exp(-md.interest_rate * maturity) * norm.pdf(d2) / (md.spot*volatility*np.sqrt(maturity))
    gamma_digital = payoff_type*((-(pd.fixed_payout*d2*np.exp(-md.interest_rate * maturity)*norm.pdf(d2))
                     - pd.fixed_payout*np.exp(-md.interest_rate * maturity)*norm.pdf(d2)*volatility*np.sqrt(maturity))/
                     (volatility*volatility*maturity*md.spot*md.spot))
    vega_digital = -payoff_type * pd.fixed_payout * np.exp(-md.interest_rate * maturity) \
                   * norm.pdf(d2) * d1 / volatility
    option_value = payoff_type*pd.fixed_payout*np.exp(- md.interest_rate * maturity) *norm.cdf(payoff_type * d2)
    log_file_output = {
        "option_value": option_value,
        "delta_value": delta_digital,
        "gamma_value": gamma_digital,
        "vega_value": vega_digital
    }
    return log_file_output

def digital_asset_or_nothing(md: market_data, pd: digitalOption, vo: vol_fetcher):
    if pd.is_call == True:
        payoff_type = 1
    else:
        payoff_type = -1
    maturity = daycount(md.val_date, pd.maturity, pd.dayCountConvention)
    volatility = vo.retrieve_vol(md.spot, maturity)

    d1 = (np.log(md.spot / pd.strike) + (md.interest_rate - md.div_yield + 0.5 * np.pow(volatility, 2)) * maturity)/ (volatility * np.sqrt(maturity))

    option_value = payoff_type*np.exp(- md.div_yield * maturity) *norm.cdf(payoff_type * d1)*md.spot
    log_file_output = {
        "option_value": option_value
    }
    return log_file_output
