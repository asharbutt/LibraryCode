#pragma once

#include <vector>
#include <stdexcept>

double linear_interp(double x1, const std::vector<double>& x, const std::vector<double>& y) { // assumes sorted vectors
    // boundary checks:
    if (x1<x[0] || x1 > x.back()) {
        throw std::invalid_argument("Input value is out of interpolation bounds");
    }
    else if (x1 == x.back()) {
        return y.back();
    }
    
    // first search for index where x1 should sit:
    int left = 0;
    for (int i = 0; i < x.size(); i++) {
        if (x1 < x[i]) {
            left = i-1;
            break;
        }
    }
    return y[left] + ((x1 - x[left]) * (y[left + 1] - y[left])) / (x[left + 1] - x[left]);
}
