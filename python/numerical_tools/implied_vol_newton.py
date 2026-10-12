import black_scholes as bs
import contract_id_class as id
import marketData as md

def newton_raphson_implied_volatility(contract: id.OptionContract, data: md.MarketData, initial_guess: float ):
    # checks to ensure contract details are sufficient
    if any(x is None for x in (contract.contractID, contract.Notional, contract.Strike, contract.instrument, contract.contractValue, contract.dateMaturity)):
        raise ValueError("Missing parameters in Contract details")
    if any(x is None for x in (data.spot, data.interestRate, data.divYield, data.valDate, data.dayCountConvention)):
        raise ValueError("Missing parameters in marketData details")
    tol = 1e-5
    max_iterations = 10000
    x_0 = initial_guess
    data.vol = x_0
    print(data)
    for i in range(max_iterations):
        x_1 = x_0 - (bs.bs_price(contract, data) - contract.contractValue) / bs.vega(contract, data)
        data.vol = x_1
        if abs(bs.bs_price(contract, data) - contract.contractValue) < tol:
            return x_1
        x_0 = x_1
    return None
