#pragma once

class vol_fetcher { // parent volatility class for passing a vol object to pricers
public:
    virtual const double retrieve_vol(double time, double spot) const = 0;
    virtual ~vol_fetcher() = default;
};

class fixed_vol : public vol_fetcher { // returns a fixed vol rather than anything
public:
    fixed_vol(double vol) : volatility(vol) {}
    const double retrieve_vol(double, double) const override {
        return volatility;
    }
private:
    double volatility;
};
