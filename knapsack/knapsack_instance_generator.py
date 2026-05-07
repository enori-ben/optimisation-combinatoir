import numpy as np
from typing import Dict, Any


def generate_knapsack_instance(n: int, rng: np.random.Generator) -> Dict[str, Any]:
    """
    Generates a single knapsack instance.
    """
    profits = rng.uniform(1, 10, size=n)
    weights = rng.uniform(1, 10, size=n)
    capacity = (5 * n) / 4

    return {
        "profits": profits,
        "weights": weights,
        "capacity": capacity
    }


def get_instances(seed: int = 42) -> Dict[int, Dict[str, Any]]:
    """
    Generates multiple knapsack instances of increasing sizes.

    Parameters:
        seed (int): Random seed for reproducibility.

    Returns:
        dict: Dictionary of instances indexed by ID.
    """

    sizes = [50, 100, 200, 500, 1000, 2000]
    rng = np.random.default_rng(seed)

    instances = {
        i + 1: generate_knapsack_instance(n, rng)
        for i, n in enumerate(sizes)
    }

    return instances