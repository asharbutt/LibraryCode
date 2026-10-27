#pragma once

#include <string>
#include <vector>
#include <algorithm>

struct options {
    std::string tradeID;
    bool is_call;
    double notional = 0.0;
    double strike;
    std::string maturity;
    std::string dayCountConvention;

    virtual const double payoff(double spot) const = 0;
    virtual const std::vector<double> payoff(std::vector<double> spot) const = 0;
};

struct vanillaEquityOption: options {

    const double payoff(double spot) const {
        if (is_call){ return std::max(spot - strike, 0.0);}
        else {return std::max(strike - spot, 0.0);}
    }
    const std::vector<double> payoff(const std::vector<double>spot) const {
        std::vector<double> payoff_vector;
        payoff_vector.resize(spot.size());

        for (size_t i = 0; i < spot.size(); i++) {
            payoff_vector[i] = payoff(spot[i]);
           
        }
        return payoff_vector;
    }
};
