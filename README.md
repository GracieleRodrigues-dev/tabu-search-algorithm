# Tabu Search Algorithm for Combinatorial Optimization

This project implements a Tabu Search algorithm to solve combinatorial optimization problems. The algorithm reads problem instances, performs multiple replicates to ensure robustness, and saves the results to an output file. Below are the instructions for compiling and running the algorithm.

---

## Features
- **Dynamic Neighbor Exploration**: Explores possible solutions by toggling element states.
- **Tabu List with Aspiration**: Prevents revisiting solutions unless they improve the global best.
- **Batch Processing**: Handles multiple instances stored in a directory.
- **Performance Metrics**: Computes the best score, mean score, and mean execution time across replicates.

---

## Dependencies
Ensure you have Python 3.8 or newer installed, along with the following packages:
- `numpy`: for numerical operations.
- `collections`: for Tabu list implementation.
- `time`: to measure execution times.

Install dependencies with:
```bash
pip install numpy
```

Run the script:
```bash
python tabu.py
```