from dataclasses import dataclass

@dataclass
class MarketData:
    spot: float
    vol: float
    interestRate: float
    divYield: float
    valDate: str


