#pragma once

#include <string>

struct market_data {
    std::string val_date;
    double spot;
    double repo_rate;
    double interest_rate;
    double div_yield;
};
