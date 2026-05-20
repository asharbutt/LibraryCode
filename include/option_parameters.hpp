#pragma once

// header file to contain the structs used to price a black scholes option

namespace option_parameters {

    struct OptionContract {
        double strike;
        double timeMaturity;
        int optionType; // +1 or -1
    };

    struct OptionsMarketData {
        double volatility;
        double interestRate;
        double divYield;
        double spot;
    };
}
