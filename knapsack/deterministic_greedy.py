import numpy as np

from knapsack.knapsack_strategy import Strategy


class DeterministicGreedyStrategy(Strategy):

    def solve(self, instance: dict) -> dict:
        """
        Solves the 0/1 Knapsack Problem
        using a deterministic greedy heuristic.
        """

        # =====================================================
        # Extract problem data
        # =====================================================
        profits = instance["profits"]
        weights = instance["weights"]
        capacity = instance["capacity"]

        n_items = len(profits)

        # =====================================================
        # Compute profit-to-weight ratios
        # =====================================================
        ratios = profits / weights

        # Sort items by descending ratio
        sorted_indices = np.argsort(-ratios)

        # =====================================================
        # Initialize solution
        # =====================================================
        current_weight = 0
        decision_array = np.zeros(n_items, dtype=int)

        # =====================================================
        # Greedy selection
        # =====================================================
        for idx in sorted_indices:

            item_weight = weights[idx]

            # Check capacity constraint
            if current_weight + item_weight <= capacity:

                # Select item
                decision_array[idx] = 1

                # Update current weight
                current_weight += item_weight

        # =====================================================
        # Compute total profit
        # =====================================================
        total_profit = int(np.dot(profits, decision_array))

        # =====================================================
        # Return final solution
        # =====================================================
        return {
            "profit": total_profit,
            "weight": current_weight,
            "decision": decision_array
        }