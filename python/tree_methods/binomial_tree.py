from parameter_files.marketData import *
from parameter_files.tradeParameters import *
from parameter_files.daycount_convention import *
from parameter_files.vol_fetcher import *
from abc import ABC, abstractmethod

class binomial_tree(ABC):
    @abstractmethod
    def price(self):
        ...
    @abstractmethod
    def calculate_delta(self):
        ...
    @abstractmethod
    def calculate_vega(self):
        ...
    @abstractmethod
    def generate_stock_prices(self):
        ...
    @abstractmethod
    def price_option(self):
        ...

class european_binomial_tree(binomial_tree):
    def __init__(self, data: market_data, params: Trade, num_steps: int, vol_object: vol_fetcher):
        self.data = data
        self.num_steps = num_steps
        self.maturity = daycount(data.val_date, params.maturity, params.dayCountConvention)
        self.params = params
        self.final_stock_vector = np.zeros(self.num_steps+1)
        self.up = np.exp(vol_object.retrieve_vol(self.params.strike, self.maturity)*(np.sqrt(daycount(data.val_date, params.maturity, params.dayCountConvention)/num_steps)))
        self.down = np.pow(self.up,-1)
        self.option_price_vector = np.zeros(self.num_steps)
        self.vol_fetcher = vol_object
        self.option_matrix_temp = []
        if self.data.repo_rate is not None:
            self.financing_rate = self.data.repo_rate
        else:
            self.financing_rate = self.data.interest_rate
        self.time_step = self.maturity / self.num_steps
        self.probability_up = (np.exp((self.financing_rate-self.data.div_yield)*self.time_step)-self.down)/(self.up - self.down)
        self.output_log = {}

        # bump and reprice parameters:
        self.dS = self.data.spot * 0.001 # bump by 10 basis points
        self.dVol = 0.01
        self.dDay = 1/365 # 1 day bump
    def price(self):
        self.generate_stock_prices()
        self.price_option()
        option_price = self.option_price_vector[0]
        self.output_log = {
            "Output Price": option_price,
            "Up move size": self.up,
            "Down move size": self.down,
            "Time step": self.time_step,
            "Time Step": self.time_step
        }
        self.calculate_delta()
        self.calculate_vega()

        return self.output_log
    def calculate_delta(self):
        original_spot = self.data.spot
        # bump and reprice for sensitivities:
        self.data.spot = original_spot + self.dS
        self.generate_stock_prices()
        self.price_option()
        bumped_up_price = self.option_price_vector[0]

        self.data.spot = original_spot - self.dS
        self.generate_stock_prices()
        self.price_option()
        bumped_down_price = self.option_price_vector[0]
        self.output_log["Delta"] = (bumped_up_price - bumped_down_price) / (2 * self.dS)

        self.data.spot = original_spot # revert the spot back to original data

        return None
    def calculate_vega(self):
        original_vol = self.vol_fetcher.retrieve_vol(self.params.strike, self.maturity)
        original_up = self.up
        original_down = self.down
        original_probability_up = self.probability_up

        self.up = np.exp((original_vol + self.dVol) * (
            np.sqrt(daycount(self.data.val_date, self.params.maturity, self.params.dayCountConvention) / self.num_steps)))
        self.down = np.pow(self.up, -1)
        self.probability_up = (np.exp((self.financing_rate-self.data.div_yield)*self.time_step) - self.down) / (self.up - self.down)
        # bump and reprice for sensitivities:
        self.generate_stock_prices()
        self.price_option()
        bumped_up_price = self.option_price_vector[0]

        self.up = np.exp((original_vol - self.dVol) * (
            np.sqrt(
                daycount(self.data.val_date, self.params.maturity, self.params.dayCountConvention) / self.num_steps)))
        self.down = np.pow(self.up, -1)
        self.probability_up = (np.exp((self.financing_rate-self.data.div_yield)*self.time_step) - self.down) / (self.up - self.down)
        self.generate_stock_prices()
        self.price_option()
        bumped_down_price = self.option_price_vector[0]
        self.output_log["Vega"] = (bumped_up_price - bumped_down_price) / (2 * self.dVol) * 0.01

        self.up =  original_up # revert the spot back to original data
        self.down = original_down
        self.probability_up = original_probability_up
        return None

    def price_option(self):
        self.option_price_vector_temp = self.params.payoff(self.final_stock_vector)

        for i in range(self.num_steps - 1, -1, -1):
            for j in range(i + 1):
                self.option_price_vector[j] = np.exp(-self.data.interest_rate * self.time_step) * (
                            (self.option_price_vector_temp[j] * self.probability_up) + (
                                self.option_price_vector_temp[j + 1] * (1 - self.probability_up)))
            self.option_price_vector_temp = self.option_price_vector

        return self.output_log

    def generate_stock_prices(self):
        for i in range(self.num_steps+1):
            self.final_stock_vector[i] = self.data.spot*np.pow(self.up,self.num_steps-i)*np.pow(self.down,i)

market_data_object = market_data(spot=100, interest_rate=0.05, div_yield=0.0,
                                        val_date="26/09/2026")
trade1_parameters = vanillaEquityOption(tradeID="trade1", is_call=True, notional=100, strike=100,
                                                     maturity="26/09/2027", dayCountConvention="A360")
vol_object = fixed_vol_fetcher(0.3)

a = european_binomial_tree(market_data_object, trade1_parameters, 1000, vol_object)
output = a.price()
print(output)