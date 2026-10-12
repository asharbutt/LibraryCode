#pragma once

#include <vector>

namespace Matrix{
    template <typename T>
    class Matrix {

    private:
        std::vector<T> matrix;
        std::size_t rows;
        std::size_t columns;

    public: 
        std::size_t rows_ = rows;
        std::size_t columns_ = columns;
        Matrix(std::size_t i, std::size_t j) : rows(i), columns(j) {
            matrix.resize(rows*columns); //resize the matrix, column major
        }

        T& operator() (std::size_t i, std::size_t j) {
            return matrix[j*rows + i];
        }
    };

    struct simulation_parameters {
        int num_sims;
        int time_steps;

    };  

    struct monte_carlo_results {
        double average;
        double std_error;

    };
}
