#pragma once

#include <cmath>
#include <algorithm>
#include <vector>
#include "option_parameters.hpp"
#include "option_parameters.hpp"
#include "Matrix.hpp"

namespace european_binomial {
    double binomialTreeEuropean(option_parameters::binomial_parameters& params, option_parameters::OptionsMarketData& data, option_parameters::OptionContract& contract) {
        params.deltaT = contract.timeMaturity / params.numSteps;
        params.up = std::exp(data.volatility * std::sqrt(params.deltaT));
        params.down = std::exp(-data.volatility * std::sqrt(params.deltaT));
        params.probabilityUp = (std::exp(data.interestRate * params.deltaT) - params.down) / (params.up - params.down);
    
        std::vector<double> optionValue(params.numSteps+1, 0.0); // initial payoff, will then be used to compute the option value at each Delta T
        std::vector<double> optionValue_temp(params.numSteps+1, 0.0); // temporary option value vector, used to hold option values from previous time.

        std::vector<double> finalStockVector(params.numSteps+1);
   
        for (std::size_t i = 0; i < params.numSteps; i++) {
            finalStockVector[i] = data.spot * std::pow(params.up, params.numSteps - i) * std::pow(params.down, i);
        }
    
        //calculate payoff on initial vector
        for (std::size_t i = 0; i <= params.numSteps; i++) {
            optionValue[i] = std::max(contract.optionType * (finalStockVector[i] - contract.strike), 0.0);
        }   

        for (std::size_t j = params.numSteps; j > 0; j--) {
            for (std::size_t i = 0; i < j; i++) {
                optionValue[i] = (optionValue[i] * params.probabilityUp + optionValue[i + 1] * (1 - params.probabilityUp)) * std::exp(-data.interestRate * params.deltaT);
            }
        }

        return optionValue[0];
    }
}

namespace american_binomial {
    double binomialTreeAmerican(option_parameters::binomial_parameters& params, option_parameters::OptionsMarketData& data,option_parameters::OptionContract& contract) {
    params.deltaT = contract.timeMaturity / params.numSteps;
    params.up = std::exp(data.volatility * std::sqrt(params.deltaT));
    params.down = std::exp(-data.volatility * std::sqrt(params.deltaT));
    params.probabilityUp = (std::exp(data.interestRate * params.deltaT) - params.down) / (params.up - params.down);

    std::vector<double> optionValue(params.numSteps + 1, 0.0); // initial payoff, will then be used to compute the option value at each Delta T
    std::vector<double> optionValue_temp(params.numSteps + 1, 0.0); // temporary option value vector, used to hold option values from previous time.

    Matrix::Matrix<double> finalStockMatrix(params.numSteps + 1, params.numSteps + 1);

    finalStockMatrix(0, 0) = data.spot;

    // initialise the stock matrix
    for (std::size_t j = 1; j <= params.numSteps; j++) {
        for (std::size_t i = 0; i < params.numSteps; i++) {
            if (i == 0) {
                finalStockMatrix(i, j) = finalStockMatrix(i, j - 1) * params.up;
            }
            else {
                finalStockMatrix(i, j) = finalStockMatrix(i - 1, j - 1) * params.down;
            }
        }
    }
    //calculate payoff on initial vector
    for (std::size_t i = 0; i <= params.numSteps; i++) {
        optionValue[i] = std::max(contract.optionType * (finalStockMatrix(i, params.numSteps) - contract.strike), 0.0);
    }

    for (std::size_t j = params.numSteps; j > 0; j--) {
        for (std::size_t i = 0; i < j; i++) {
            optionValue[i] = std::max((optionValue[i] * params.probabilityUp + optionValue[i + 1] * (1 - params.probabilityUp)) * std::exp(-data.interestRate * params.deltaT), std::max(contract.optionType*(finalStockMatrix(i,j-1)-contract.strike),0.0));
        }
    }

    return optionValue[0];
}
}
