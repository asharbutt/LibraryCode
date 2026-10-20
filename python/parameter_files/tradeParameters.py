from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional
import numpy as np

@dataclass
class Trade:
    tradeID: str
    is_call: bool  # +1 for call, -1 for put
    notional: float
    dayCountConvention: str
    product_type = ""
    maturity = ""

    @abstractmethod
    def payoff(self, spot):
        ...

@dataclass(kw_only=True)
class vanillaEquityOption(Trade):
    tradeID: str
    is_call: bool # +1 for call, -1 for put
    notional: float
    strike: float
    maturity: str # this should be a date, we calculate the daycount on the fly using a daycount conventions module
    dayCountConvention: str
    product_type = "vanilla_equity_option"# single_equity_product
    process_scheme = "euler"

    def payoff(self, spot):
        return np.maximum((spot - self.strike),0.0) if self.is_call else np.maximum(self.strike - spot, 0.0)

@dataclass(kw_only=True)
class digitalOption(Trade):
    tradeID: str
    is_call: bool  # +1 for call, -1 for put
    notional: float
    fixed_payout: float

    strike: float
    maturity: str # this should be a date, we calculate the daycount on the fly using a daycount conventions module
    dayCountConvention: str
    product_type = "digital_option"# single_equity_product
    process_scheme = "euler"

    def payoff(self, spot):
        indicator_vector = np.heaviside(spot - self.strike, 0) if self.is_call else  np.heaviside(self.strike - spot, 0)
        return indicator_vector*self.fixed_payout

@dataclass(kw_only=True)
class assetornothingOption(Trade):
    tradeID: str
    is_call: bool  # +1 for call, -1 for put
    notional: float
    strike: float
    maturity: str # this should be a date, we calculate the daycount on the fly using a daycount conventions module
    dayCountConvention: str
    product_type = "digital_option"# single_equity_product
    process_scheme = "euler"

    def payoff(self, spot):
        indicator_vector = np.heaviside(spot - self.strike, 0) if self.is_call else np.heaviside(self.strike - spot, 0)
        return indicator_vector * spot

@dataclass(kw_only=True)
class vanillaAmericanOption(Trade):
    tradeID: str
    is_call: bool  # +1 for call, -1 for put
    notional: float
    strike: float
    maturity: str  # this should be a date, we calculate the daycount on the fly using a daycount conventions module
    dayCountConvention: str
    product_type = "vanilla_equity_option"  # single_equity_product
    process_scheme = "euler"

    def payoff(self, spot):
        return np.maximum((spot - self.strike), 0.0) if self.is_call else np.maximum(self.strike - spot, 0.0)

@dataclass(kw_only=True)
class up_out_barrier_option(Trade):
    tradeID: str
    is_call: bool  # +1 for call, -1 for put
    notional: float
    barrier: float
    barrier_type: str
    strike: float
    maturity: str  # this should be a date, we calculate the daycount on the fly using a daycount conventions module
    dayCountConvention: str
    product_type = "vanilla_equity_option"  # single_equity_product
    process_scheme = "exponential_CIR"

    def payoff(self, spot):
        return np.maximum((spot - self.strike), 0.0) if self.is_call else np.maximum(self.strike - spot, 0.0)

@dataclass(kw_only=True)
class geometricAsianOption(Trade):
    tradeID: str
    is_call: bool  # +1 for call, -1 for put
    notional: float
    strike_type: str # either fixed or float
    strike: float
    maturity: str  # this should be a date, we calculate the daycount on the fly using a daycount conventions module
    dayCountConvention: str
    observation_type: str  # Continuous, daily etc
    observation_dates: []
    product_type = "vanilla_equity_option"  # single_equity_product
    process_scheme = "euler"

    def payoff(self, spot):
        return np.maximum((spot - self.strike), 0.0) if self.is_call else np.maximum(self.strike - spot, 0.0)


@dataclass(kw_only=True)
class arithmeticAsianOption(Trade):
    tradeID: str
    is_call: bool  # +1 for call, -1 for put
    notional: float
    strike_type: str  # either fixed or float
    strike: float
    maturity: str  # this should be a date, we calculate the daycount on the fly using a daycount conventions module
    dayCountConvention: str
    observation_dates: []
    observation_type: str # Continuous, daily etc
    product_type = "vanilla_equity_option"  # single_equity_product
    process_scheme = "euler"

    def payoff(self, spot):
        return np.maximum((spot - self.strike), 0.0) if self.is_call else np.maximum(self.strike - spot, 0.0)
