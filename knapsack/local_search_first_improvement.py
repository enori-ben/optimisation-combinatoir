import numpy as np
import itertools

from knapsack.knapsack_strategy import Strategy
from knapsack.nondeterministic_greedy import NonDeterministicGreedyStrategy


class LocalSearchFirstImprovement(Strategy):

    # =========================================================
    # Move evaluation (core reusable function)
    # =========================================================
    def _evaluate_move(self, solution, weights, profits, capacity, drop, add):

        weight_delta = 0
        profit_delta = 0

        for i in drop:
            weight_delta -= weights[i]
            profit_delta -= profits[i]

        for j in add:
            weight_delta += weights[j]
            profit_delta += profits[j]

        new_weight = solution["weight"] + weight_delta

        if new_weight > capacity:
            return None

        return {
            "profit": solution["profit"] + profit_delta,
            "weight": new_weight,
            "move": (drop, add)
        }

    # =========================================================
    # Neighbor generator (streaming, no storage)
    # =========================================================
    def generate_neighbors(self, instance, solution):

        decision = solution["decision"]
        weights = instance["weights"]
        profits = instance["profits"]
        capacity = instance["capacity"]

        inside = np.where(decision == 1)[0]
        outside = np.where(decision == 0)[0]

        eval_move = lambda d, a: self._evaluate_move(
            solution, weights, profits, capacity, d, a
        )

        # -------------------------
        # 1-out / 1-in
        # -------------------------
        for i in inside:
            for j in outside:
                n = eval_move([i], [j])
                if n:
                    yield n

        # -------------------------
        # 1-out / 2-in
        # -------------------------
        for i in inside:
            for a in itertools.combinations(outside, 2):
                n = eval_move([i], list(a))
                if n:
                    yield n

        # -------------------------
        # 2-out / 1-in
        # -------------------------
        for d in itertools.combinations(inside, 2):
            for j in outside:
                n = eval_move(list(d), [j])
                if n:
                    yield n

        # -------------------------
        # 2-out / 2-in
        # -------------------------
        for d in itertools.combinations(inside, 2):
            for a in itertools.combinations(outside, 2):
                n = eval_move(list(d), list(a))
                if n:
                    yield n

    # =========================================================
    # Solver (First Improvement)
    # =========================================================
    def solve(self, instance: dict) -> dict:

        greedy = NonDeterministicGreedyStrategy()
        solution = greedy.solve(instance)

        while True:

            improved = False

            for neighbor in self.generate_neighbors(instance, solution):

                if neighbor["profit"] > solution["profit"]:

                    drop, add = neighbor["move"]

                    for i in drop:
                        solution["decision"][i] = 0

                    for j in add:
                        solution["decision"][j] = 1

                    solution["profit"] = neighbor["profit"]
                    solution["weight"] = neighbor["weight"]

                    improved = True
                    break  # FIRST improvement

            if not improved:
                break

        return solution