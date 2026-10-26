// If MATRIX_H is not defined, define it (start of header guard)
#ifndef MATRIX_H

// Define MATHUTILS_H to prevent multiple inclusions
#define MATRIX_H

#include <iostream>
#include <vector>
#include <stdexcept>

class Matrix {
public:
    Matrix(size_t i, size_t j) : rows_(i), columns_(j) { // create a matrix in vector format populated with 0
        matrix_.resize(i * j, 0.0);
    }
    double& operator() (std::size_t i, std::size_t j) { // The matrix is row major
            return matrix_[i * columns_ + j];
        }
    const double& operator()(std::size_t i, std::size_t j) const { // The matrix is row major
        return matrix_[i * columns_ + j];
    }
        size_t columns() const { return columns_; }
        size_t rows() const { return rows_; }
    Matrix operator+ (const Matrix& m) const {
        if (m.rows() != rows_ || m.columns() != columns_) {
            throw std::invalid_argument("Matrix dimensions do not match!");
        }
        else {
            Matrix sum(rows_, columns_);
            for (std::size_t i = 0; i < rows_; i++) {
                for (std::size_t j = 0; j < columns_; j++) {
                    sum(i, j) = (*this)(i, j) + m(i, j);
                }
            }
            return sum;
        }
    }
    Matrix operator*(const Matrix& m) const{
        if (columns_ != m.rows()) {
            throw std::invalid_argument("Matrix row number does not align with column numbers");
        }
        Matrix product(rows_, m.columns());
        for (std::size_t other_column = 0; other_column < m.columns(); other_column++) {
            for (std::size_t i = 0; i < rows_; i++) {
                for (std::size_t j = 0; j < columns_; j++) {
                    product(i, other_column) += (*this)(i, j) * m(j, other_column);
                }
            }

        }
        return product;
    }
    friend std::ostream& operator<<(std::ostream& os, Matrix& matrix) {
        for (std::size_t i = 0; i < matrix.rows(); i++) {
            for (std::size_t j = 0; j < matrix.columns(); j++) {
                os << matrix(i, j);
                if (j + 1 < matrix.columns()) os << ", ";
            }
            os << "\n";
        }
        return os;
    }
private:
    std::vector<double>matrix_;
    std::size_t rows_;
    std::size_t columns_;
};

/*
Sample code for how to use the matrix
int main()
{
    Matrix m(2, 2);
    int a = 0;
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            m(i, j) = a;
            a++;
        }
    }
    a = 0;
    Matrix d(2, 2);
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            d(i, j) = a;
            a++;
        }
    }
    Matrix C = d * m;

    std::cout << C;

}
*/

#endif
