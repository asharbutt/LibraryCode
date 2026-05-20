#pragma once

#include <cmath>      
#include "option_parameters.hpp"
#include "statistics.hpp"

namespace black_scholes_merton {

    double compute_d1(const option_parameters::OptionContract& c, const option_parameters::OptionsMarketData& d) { return (std::log(d.spot / c.strike) + (d.interestRate - d.divYield + 0.5 * d.volatility * d.volatility) * c.timeMaturity) / (d.volatility * std::sqrt(c.timeMaturity)); }
    double price(const option_parameters::OptionContract& c, const option_parameters::OptionsMarketData& d) {
        const double d1 = compute_d1(c, d);
        const double d2 = d1 - d.volatility * std::sqrt(c.timeMaturity);
        return c.optionType * d.spot * std::exp(-d.divYield * c.timeMaturity) * stats::standard_normal_cdf(c.optionType * d1) - c.optionType * c.strike * std::exp(-d.interestRate * c.timeMaturity) * stats::standard_normal_cdf(c.optionType * d2);
    }
    double delta(const option_parameters::OptionContract& c, const option_parameters::OptionsMarketData& d) { return c.optionType * std::exp(-d.divYield * c.timeMaturity) * stats::standard_normal_cdf(c.optionType * compute_d1(c, d)); }
    double gamma(const option_parameters::OptionContract& c, const option_parameters::OptionsMarketData& d) { return stats::standard_normal_pdf(compute_d1(c, d)) / (d.spot * d.volatility * std::sqrt(c.timeMaturity)); }
    double vega(const option_parameters::OptionContract& c, const option_parameters::OptionsMarketData& d) { return d.spot * std::exp(-d.divYield * c.timeMaturity) * stats::standard_normal_pdf(compute_d1(c, d)) * std::sqrt(c.timeMaturity); }

}
