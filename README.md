# Project Setup Guide

## Prerequisites

Make sure you have **Python 3.8+** installed on your system.

---

## 1. Create a Python Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

- **Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

---

## 2. Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

---

## 3. TSP Instances

The TSP benchmark instances are already included in the `tsplib-master/` folder located in the **root directory** of this project. They are sourced from the [TSPLIB repository](https://github.com/mastqe/tsplib) by mastqe.

Your project structure should look like this:

```
project-root/
├── tsplib-master/
│   ├── att48.tsp
│   ├── berlin52.tsp
│   ├── ...
├── venv/
├── requirements.txt
└── README.md
```

---

## 4. Project Architecture — Strategy Pattern

The project is built around the **Strategy design pattern**. A common `Strategy` interface defines a `solve()` method, and each metaheuristic algorithm is implemented as a concrete class that fulfills this contract.

The algorithms are organized by problem under their respective folders:

- `tsp/` — contains the algorithm classes for the Travelling Salesman Problem
- `knapsack/` — contains the algorithm classes for the Binary Knapsack Problem

In each folder, every class corresponds to a specific metaheuristic algorithm, and its name directly reflects the algorithm being used (e.g. a class named `SimulatedAnnealing` implements Simulated Annealing). All of them implement the `solve()` method defined by the `Strategy` interface, making it straightforward to swap or extend algorithms without modifying the rest of the codebase.

---

## 5. Running the Project

### Step 1 — Generate TSP Adjacency Matrices

Before running the TSP problem, you need to generate the adjacency matrices from the raw `.tsp` instance files. Run:

```bash
python3 tsp/tsp_instance_generator.py
```

This will parse all TSP instances using a lexer and parser, and generate the corresponding adjacency matrices as `.csv` files, located under:

```
tsp/tsplib-master/adj_matrices/
```

### Step 2 — Run the TSP Problem

Once the adjacency matrices are generated, run the TSP problem against all algorithms with:

```bash
python3 main.py --problem tsp --instances tsp/tsplib-master/adj_matrices
```

### Run the Knapsack Problem

To run the Knapsack problem against all algorithms:

```bash
python3 main.py --problem knapsack
```

---

## 6. Viewing Results Without Running the Code

If you want to consult the results without running the code, pre-computed result files are available at the root of the project:

- **TSP results** → `tsp_results.csv`
- **Knapsack results** → `knapsack_results.csv`
