import numpy as np
from parameter_files import tradeParameters as pd
from abc import ABC, abstractmethod

class vol_fetcher(ABC):
    @abstractmethod
    def retrieve_vol(self, spot, maturity):
        ...

class fixed_vol_fetcher(vol_fetcher):
    def __init__(self, vol):
        self.vol = vol
    def retrieve_vol(self, spot, maturity):
        return self.vol

class local_vol_fetcher(vol_fetcher):
    def __init__(self, implied_vol_matrix):
        self.implied_vol_matrix = implied_vol_matrix
    def retrieve_vol(self,spot, maturity):
        pass
