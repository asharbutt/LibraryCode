from dataclasses import dataclass
from typing import Optional

@dataclass
class market_data: # We maintain this class as optional, which is updated on the fly. In reality, i think we would assume that a market data module inputs the information into here live
    spot: Optional[float] = None
    repo_rate: Optional[float] = None
    interest_rate: Optional[float] = None
    div_yield: Optional[float] = None
    val_date: Optional[str] = None
