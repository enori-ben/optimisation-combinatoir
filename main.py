import argparse
import sys
from pathlib import Path
from typing import Dict, Generator, Tuple, Any

import numpy as np
import pandas as pd

# =========================
# TSP Imports
# =========================
from tsp.deterministic_greedy import DeterministicGreedyStrategy
from tsp.nondeterministic_greedy import NonDeterministicGreedyStrategy
from tsp.local_search_best_improvement import LocalSearchBestImprovement
from tsp.local_search_first_improvement import LocalSearchFirstImprovement
from tsp.simulated_annealing import SimulatedAnnealing
from tsp.genetic import GeneticStrategy

# =========================
# Knapsack Imports
# =========================
from knapsack.knapsack_instance_generator import get_instances

from knapsack.deterministic_greedy import (
    DeterministicGreedyStrategy as KSDetGreedy,
)
from knapsack.nondeterministic_greedy import (
    NonDeterministicGreedyStrategy as KSNDGreedy,
)
from knapsack.local_search_best_improvement import (
    LocalSearchBestImprovement as KSLSBest,
)
from knapsack.local_search_first_improvement import (
    LocalSearchFirstImprovement as KSLSFirst,
)
from knapsack.simulated_annealing import (
    SimulatedAnnealing as KSSA,
)
from knapsack.genetic import (
    GeneticStrategy as KSGenetic,
)

# =========================================================
# Strategy Registries
# =========================================================

TSP_STRATEGIES = {
    "det_greedy": DeterministicGreedyStrategy,
    "nd_greedy": NonDeterministicGreedyStrategy,
    "ls_best": LocalSearchBestImprovement,
    "ls_first": LocalSearchFirstImprovement,
    "sa": SimulatedAnnealing,
    "genetic": GeneticStrategy,
}

KNAPSACK_STRATEGIES = {
    "det_greedy": KSDetGreedy,
    "nd_greedy": KSNDGreedy,
    "ls_best": KSLSBest,
    "ls_first": KSLSFirst,
    "sa": KSSA,
    "genetic": KSGenetic,
}

# =========================================================
# Instance Loaders
# =========================================================

def load_tsp_instances(
    directory_path: str,
) -> Generator[Tuple[str, np.ndarray], None, None]:
    """
    Load all TSP CSV instances from a directory.
    """
    directory = Path(directory_path)

    for file in directory.glob("*.csv"):
        try:
            data = np.loadtxt(file, delimiter=",")
            yield file.name, data
        except Exception as error:
            print(f"[WARNING] Failed to load {file.name}: {error}")


def load_knapsack_instances() -> Dict[Any, Any]:
    """
    Load all knapsack instances.
    """
    return get_instances()


# =========================================================
# Generic Experiment Runner
# =========================================================

def run_experiments(
    instances,
    strategies: Dict[str, Any],
    metric_key: str,
    instance_label: str,
) -> list:
    """
    Execute all strategies on all instances.
    """
    results = []

    for instance_name, instance_data in instances:

        print(f"\n[INFO] Processing instance: {instance_name}")

        for strategy_name, strategy_class in strategies.items():

            print(f"   -> Running strategy: {strategy_name}")

            strategy = strategy_class()
            result = strategy.solve(instance_data)

            results.append({
                instance_label: instance_name,
                "strategy": strategy_name,
                metric_key: result[metric_key],
            })

    return results


# =========================================================
# TSP Pipeline
# =========================================================

def run_tsp(instance_directory: str) -> None:

    tsp_instances = load_tsp_instances(instance_directory)

    results = run_experiments(
        instances=tsp_instances,
        strategies=TSP_STRATEGIES,
        metric_key="distance",
        instance_label="instance_name",
    )

    output_file = "tsp_results.csv"

    pd.DataFrame(results).to_csv(output_file, index=False)

    print(f"\n[INFO] Results saved to {output_file}")


# =========================================================
# Knapsack Pipeline
# =========================================================

def run_knapsack() -> None:

    raw_instances = load_knapsack_instances()

    # Convert dict.items() into iterable format
    instances = raw_instances.items()

    results = run_experiments(
        instances=instances,
        strategies=KNAPSACK_STRATEGIES,
        metric_key="profit",
        instance_label="instance_id",
    )

    output_file = "knapsack_results.csv"

    pd.DataFrame(results).to_csv(output_file, index=False)

    print(f"\n[INFO] Results saved to {output_file}")


# =========================================================
# CLI
# =========================================================

def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Optimization Problem Solver"
    )

    parser.add_argument(
        "--problem",
        required=True,
        choices=["tsp", "knapsack"],
        help="Optimization problem to solve.",
    )

    parser.add_argument(
        "--instances",
        type=str,
        help="Directory containing TSP instances.",
    )

    return parser.parse_args()


# =========================================================
# Main
# =========================================================

def main():

    args = parse_arguments()

    if args.problem == "tsp":

        if not args.instances:
            print(
                "[ERROR] TSP requires --instances <directory_path>"
            )
            sys.exit(1)

        run_tsp(args.instances)

    elif args.problem == "knapsack":
        run_knapsack()


if __name__ == "__main__":
    main()