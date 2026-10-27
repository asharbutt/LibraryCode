# LibraryCode

Pricing code shown in the [Numerical lab](https://asharbutt.github.io/portfolio/code.html) on my portfolio site. Closed-form, tree and Monte Carlo methods for vanilla and exotic options, in C++ and Python.

## Layout

```
cpp/
  include/
    options.hpp               option base struct and vanilla equity payoff
    market_data.hpp           valuation date, spot, rates, dividend yield
    option_parameters.hpp     contract, market data and binomial tree structs
    Matrix.hpp                simple row-major matrix
    statistics.hpp            normal pdf / cdf
    black_scholes_merton.hpp  closed-form price and Greeks
    tree_methods.hpp          European and American binomial trees

python/
  parameter_files/            inputs shared by every pricer
    marketData.py             spot, rates, dividend yield, valuation date
    tradeParameters.py        Trade base class and option payoffs
    daycount_convention.py    A360 / A365 year fractions
    vol_fetcher.py            vol lookup (fixed vol for now)
  closed_form_pricers/
    black_scholes.py          Black-Scholes-Merton price and Greeks
    digitals.py               cash-or-nothing and asset-or-nothing digitals
  tree_methods/
    binomial_tree.py          European binomial tree with bump-and-reprice Greeks
  numerical_tools/
    implied_vol_newton.py     Newton-Raphson implied volatility
  monte_carlo/
    estimate_pi.py            Monte Carlo estimate of pi
    mc_european.py            Monte Carlo European pricer
```

## Using it

**C++** is header-only. Add `cpp/include` to the include path:

```
g++ -std=c++17 -Icpp/include main.cpp -o main
```

**Python** modules import each other by package name (`from parameter_files.marketData import *`), so run them from inside `python/`:

```
cd python
pip install -r ../requirements.txt
python -m tree_methods.binomial_tree
```

## Status

- `numerical_tools/implied_vol_newton.py` still uses the older contract and market data classes, so it won't import until it's moved onto `parameter_files`.
- `monte_carlo/mc_european.py` imports an `sde_processes` module that isn't in the repo yet.
