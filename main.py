import argparse
import sys
import numpy as np
from pathlib import Path
from typing import Generator
import pandas as pd

# TSP strategy imports 
from tsp.deterministic_greedy           import DeterministicGreedyStrategy
from tsp.nondeterministic_greedy        import NonDeterministicGreedyStrategy
from tsp.local_search_best_improvement  import LocalSearchBestImprovement
from tsp.local_search_first_improvement import LocalSearchFirstImprovement
from tsp.simulated_annealing            import SimulatedAnnealing
from tsp.genetic                        import GeneticStrategy

# Knapsack strategy imports 
from knapsack.knapsack_instance_generator import get_instances
from knapsack.deterministic_greedy           import DeterministicGreedyStrategy      as KS_DetGreedy
from knapsack.nondeterministic_greedy        import NonDeterministicGreedyStrategy   as KS_NDGreedy
from knapsack.local_search_best_improvement  import LocalSearchBestImprovement       as KS_LSBest
from knapsack.local_search_first_improvement import LocalSearchFirstImprovement      as KS_LSFirst
from knapsack.simulated_annealing            import SimulatedAnnealing               as KS_SA
from knapsack.genetic                        import GeneticStrategy                  as KS_Genetic


# Strategy maps 
TSP_STRATEGIES = {
    "det_greedy": DeterministicGreedyStrategy,
    "nd_greedy":  NonDeterministicGreedyStrategy,
    "ls_best":    LocalSearchBestImprovement,
    "ls_first":   LocalSearchFirstImprovement,
    "sa":         SimulatedAnnealing,
    "genetic":    GeneticStrategy,
}

KNAPSACK_STRATEGIES = {
    "det_greedy": KS_DetGreedy,
    "nd_greedy":  KS_NDGreedy,
    "ls_best":    KS_LSBest,
    "ls_first":   KS_LSFirst,
    "sa":         KS_SA,
    "genetic":    KS_Genetic,
}


# Instances loaders 
def tsp_instance_generator(directory_path: str):
    path_obj = Path(directory_path)
    for file in path_obj.glob("*.csv"):
        try:
            # Yielding the name alongside the data
            yield file.name, np.loadtxt(file, delimiter=",")
        except Exception:
            continue

def load_knapsack_instance() -> list:

    # get all instances (they are only 5)
    instances = get_instances()

    return instances

def main():
    parser = argparse.ArgumentParser(description="Optimization Problem Solver")

    # Positional Argument: The Problem
    parser.add_argument(
        "--problem",
        choices=["tsp", "knapsack"],
        help="The optimization problem to solve."
    )

    # Instance file (required for TSP; can be omitted for knapsack)
    parser.add_argument(
        "--instances",
        type=str,
        help="Path to the instance directory."
    )

    args = parser.parse_args()

    if args.problem == "tsp":
        if not args.instances:
            print("[ERROR] TSP requires a directory. Use --instances <path>.")
            sys.exit(1)

        # Initialize a list to store result rows
        results_data = []

        # Iterate through instances from your generator
        for file_name, instance in tsp_instance_generator(args.instances):
            
            instance_name = file_name

            print(f"Working with instance {instance_name}")

            for stg_name, stg_class in TSP_STRATEGIES.items():
                strategy = stg_class()

                print(f"Strategy: {stg_name}")
                
                result = strategy.solve(instance)
            
                # Append a dictionary for each run
                results_data.append({
                    "instance_name": instance_name,
                    "strategy": stg_name,
                    "shortest_distance": result["distance"]
                })

        # Create DataFrame and Save
        df = pd.DataFrame(results_data)
    
        df.to_csv("tsp_results.csv", index=False)
        print("[INFO] Results saved to tsp_results.csv")

    # Knapsack
    elif args.problem == "knapsack":
        
        # Initialize a list to store result rows
        results_data = []

        instances  = load_knapsack_instance()
        for i, instance in instances.items():

            print(f"Working with instance number {i}")

            for stg_name, stg_class in KNAPSACK_STRATEGIES.items():
                strategy = stg_class()

                print(f"Strategy: {stg_name}")
                
                result = strategy.solve(instance)["profit"]
            
                # Append a dictionary for each run
                results_data.append({
                    "n_instance": i,
                    "strategy": stg_name,
                    "profit": result
                })
        
        # Create DataFrame and Save
        df = pd.DataFrame(results_data)
    
        df.to_csv("knapsack_results.csv", index=False)
        print("[INFO] Results saved to knapsack_results.csv")
        


if __name__ == "__main__":
    main()