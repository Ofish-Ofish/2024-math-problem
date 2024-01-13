# 2024 Math Problem Solver 🧮

## Introduction

This Python script aims to solve the "2024 Math Problem," a challenge to use the digits 2, 0, 2, and 4, along with various mathematical operations, to create expressions that represent the counting numbers from 1 to 100.

## How to Solve the 2024 Math Problem

To solve the 2024 Math Problem, this script generates random mathematical expressions using the digits 2, 0, 2, and 4, along with operations such as addition, subtraction, multiplication, division, exponentiation, square root, factorial, and double factorial. Expressions may also include grouping symbols and multi-digit numbers.

## Code Explanation

The script utilizes the built-in `math` module for mathematical functions, the `time` module for timing calculations, the `functools` module for result caching, and the `random` library for random number generation. It employs randomness to explore various combinations of expressions until it finds solutions for all counting numbers from 1 to 100.

### Installation

Clone the repository and run the script:

```bash
$ git clone https://github.com/Ofish-Ofish/2024-math-problem.git
$ cd 2024-math-problem
$ python math_solver.py
```
## License
This project is licensed under the MIT License. 

## Results
The script outputs the discovered expressions for each counting number, along with the number of attempts and the time taken to find all solutions. Solutions are saved to a text file in the solutions directory.
