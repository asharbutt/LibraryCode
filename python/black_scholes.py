from scipy.stats import norm
from marketData import *
import contract_id_class as id
import numpy as np
import daycountConventionCalculator as cd

def bs_price(contract: id.OptionContract, data: MarketData):
    d1 = (np.log(data.spot / contract.Strike) + (data.interestRate - data.divYield + 0.5 * data.vol*data.vol)*cd.daycount(data.valDate, contract.timeMaturity, contract.dayCountConvention))/ (data.vol*np.sqrt(contract.timeMaturity))
    d2 = d1 - (data.vol*np.sqrt(contract.timeMaturity))
    return contract.optionType*data.spot*np.exp(-data.divYield*cd.daycount(data.valDate, contract.timeMaturity, contract.dayCountConvention))*norm.cdf(contract.optionType* d1) - contract.optionType*contract.Strike*np.exp(-data.interestRate*cd.daycount(data.valDate, contract.timeMaturity, data.dayCountConvention))*norm.cdf(contract.optionType* d2)

def delta(contract: id.OptionContract, data: MarketData):
    d1 = (np.log(data.spot / contract.Strike) + (
                data.interestRate - data.divYield + 0.5 * data.vol * data.vol) * contract.Strike) / (
                     data.vol * np.sqrt(contract.Strike))
    return contract.optionType*np.exp(-data.divYield*cd.daycount(data.valDate, contract.timeMaturity, contract.dayCountConvention))*norm.cdf(contract.optionType*d1)

def gamma(contract: id.OptionContract, data: MarketData):
    d1 = (np.log(data.spot / contract.Strike) + (
                data.interestRate - data.divYield + 0.5 * data.vol * data.vol) * contract.Strike) / (
                     data.vol * np.sqrt(contract.Strike))
    return norm.pdf(d1) /(data.spot*np.sqrt(contract.timeMaturity)*data.vol)

def vega(contract: id.OptionContract, data: MarketData):
    d1 = (np.log(data.spot / contract.Strike) + (
            data.interestRate - data.divYield + 0.5 * data.vol * data.vol) * contract.Strike) / (
                 data.vol * np.sqrt(contract.Strike))
    return data.spot * np.exp(-data.divYield*cd.daycount(data.valDate, contract.timeMaturity, contract.dayCountConvention))*norm.pdf(d1) * np.sqrt(contract.timeMaturity)

def theta(contract: id.OptionContract, data: MarketData):
    d1 = ((np.log(data.spot / contract.Strike) + (data.interestRate - data.divYield + 0.5 * data.vol * data.vol) * cd.daycount(data.valDate, contract.timeMaturity, contract.dayCountConvention))
          / (data.vol * np.sqrt(contract.timeMaturity)))
    d2 = d1 - (data.vol * np.sqrt(contract.timeMaturity))
    return -(data.vol * data.spot * norm.pdf(d1))/(2*np.sqrt(contract.timeMaturity)) - contract.optionType * data.interestRate * contract.Strike*np.exp(-data.interestRate*cd.daycount(data.valDate, contract.timeMaturity, contract.dayCountConvention))*norm.cdf(contract.optionType*d2)

def rho(contract: id.OptionContract, data: MarketData):
    d1 = ((np.log(data.spot / contract.Strike) + (
                data.interestRate - data.divYield + 0.5 * data.vol * data.vol) * cd.daycount(data.valDate, contract.timeMaturity, contract.dayCountConvention))
          / (data.vol * np.sqrt(contract.timeMaturity)))
    d2 = d1 - (data.vol * np.sqrt(contract.timeMaturity))
    return contract.optionType*contract.Strike*cd.daycount(data.valDate, contract.timeMaturity, contract.dayCountConvention)*np.exp(-data.interestRate*cd.daycount(data.valDate, contract.timeMaturity, contract.dayCountConvention))*norm.cdf(contract.optionType*d2)
