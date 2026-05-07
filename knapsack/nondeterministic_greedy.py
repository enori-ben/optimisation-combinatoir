import numpy as np
from knapsack.knapsack_strategy import Strategy


class NonDeterministicGreedyStrategy(Strategy):

    def solve(self, instance: dict) -> dict:

        profits = instance["profits"]
        weights = instance["weights"]
        capacity = instance["capacity"]

        n_items = len(profits)

        # -------------------------------------------------
        # Sort by profit/weight ratio
        # -------------------------------------------------
        ratios = profits / weights
        remaining = np.argsort(-ratios)

        decision = np.zeros(n_items, dtype=int)

        current_weight = 0

        # -------------------------------------------------
        # Stochastic greedy selection
        # -------------------------------------------------
        while len(remaining) > 0:

            # sample randomly from remaining items
            idx_pos = np.random.randint(len(remaining))
            item = remaining[idx_pos]

            # try to add item
            if current_weight + weights[item] <= capacity:
                decision[item] = 1
                current_weight += weights[item]

            # remove selected item (efficient swap delete)
            remaining[idx_pos] = remaining[-1]
            remaining = remaining[:-1]

        # -------------------------------------------------
        # compute profit
        # -------------------------------------------------
        total_profit = np.dot(profits, decision)

        return {
            "profit": total_profit,
            "weight": current_weight,
            "decision": decision
        }