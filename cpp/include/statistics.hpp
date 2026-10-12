#pragma once
#include <cmath>

namespace stats {

    double standard_normal_pdf(double x) {
        double pi = 3.14159265358979323846;
        return (1 / sqrt(2 * pi)) * exp(-0.5 * x * x);
    }

    double standard_normal_cdf(double x) {
        return 0.5 * erfc(-x * sqrt(0.5));
    }

    double normal_pdf(double x, double mean, double volatility) {
        double pi = 3.14159265358979323846;
        return (1 / (volatility * sqrt(2 * pi))) * exp(-0.5 * (x - mean) * (x - mean) / (volatility * volatility));
    }
}
