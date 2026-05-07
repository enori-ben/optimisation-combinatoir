import numpy as np
import random
import math

from knapsack.knapsack_strategy import Strategy
from knapsack.nondeterministic_greedy import NonDeterministicGreedyStrategy


class SimulatedAnnealing(Strategy):

    # =========================================================
    # Cooling schedule
    # =========================================================
    def cooling(self, t):
        return t * 0.95

    # =========================================================
    # Feasible random neighbor
    # =========================================================
    def get_feasible_random_neighbor(self, instance, solution):

        weights = instance["weights"]
        profits = instance["profits"]
        capacity = instance["capacity"]

        decision = solution["decision"]

        inside = np.where(decision == 1)[0].tolist()
        outside = np.where(decision == 0)[0].tolist()

        if not inside or not outside:
            return None

        move_types = [
            ("1-1", 40),
            ("1-2", 30),
            ("2-1", 20),
            ("2-2", 10)
        ]

        for _ in range(50):

            move_type = random.choices(
                [m[0] for m in move_types],
                weights=[m[1] for m in move_types]
            )[0]

            try:
                if move_type == "1-1":
                    drops = random.sample(inside, 1)
                    adds = random.sample(outside, 1)

                elif move_type == "1-2":
                    if len(outside) < 2:
                        continue
                    drops = random.sample(inside, 1)
                    adds = random.sample(outside, 2)

                elif move_type == "2-1":
                    if len(inside) < 2:
                        continue
                    drops = random.sample(inside, 2)
                    adds = random.sample(outside, 1)

                else:
                    if len(inside) < 2 or len(outside) < 2:
                        continue
                    drops = random.sample(inside, 2)
                    adds = random.sample(outside, 2)

            except ValueError:
                continue

            w_delta = (
                sum(weights[j] for j in adds)
                - sum(weights[i] for i in drops)
            )

            if solution["weight"] + w_delta > capacity:
                continue

            p_delta = (
                sum(profits[j] for j in adds)
                - sum(profits[i] for i in drops)
            )

            return {
                "p_delta": p_delta,
                "w_delta": w_delta,
                "move": (drops, adds)
            }

        return None

    # =========================================================
    # Solve
    # =========================================================
    def solve(self, instance: dict) -> dict:

        greedy = NonDeterministicGreedyStrategy()
        solution = greedy.solve(instance)

        # deep copy (IMPORTANT FIX)
        best = {
            "profit": solution["profit"],
            "weight": solution["weight"],
            "decision": solution["decision"].copy()
        }

        temperature = 100.0

        while temperature > 1e-4:

            for _ in range(len(instance["profits"]) * 10):

                neighbor = self.get_feasible_random_neighbor(instance, solution)

                if neighbor is None:
                    continue

                delta = neighbor["p_delta"]

                # Acceptance probability (stable version)
                if delta > 0:
                    accept = True
                else:
                    try:
                        prob = math.exp(delta / temperature)
                    except OverflowError:
                        prob = 0.0

                    accept = random.random() < prob

                if not accept:
                    continue

                drops, adds = neighbor["move"]

                for i in drops:
                    solution["decision"][i] = 0
                for j in adds:
                    solution["decision"][j] = 1

                solution["profit"] += neighbor["p_delta"]
                solution["weight"] += neighbor["w_delta"]

                if solution["profit"] > best["profit"]:
                    best = {
                        "profit": solution["profit"],
                        "weight": solution["weight"],
                        "decision": solution["decision"].copy()
                    }

            temperature = self.cooling(temperature)

        return best