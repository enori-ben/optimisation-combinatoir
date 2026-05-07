import math
import random
import numpy as np
from tsp.tsp_strategy import Strategy
from tsp.nondeterministic_greedy import NonDeterministicGreedyStrategy


class SimulatedAnnealing(Strategy):

    # =========================================================
    # 2-opt delta computation
    # =========================================================
    def compute_delta(self, path, i, j, adj):

        a, b = path[i], path[i + 1]
        c, d = path[j], path[j + 1]

        removed = adj[a, b] + adj[c, d]
        added = adj[a, c] + adj[b, d]

        return added - removed

    # =========================================================
    # random valid 2-opt move
    # =========================================================
    def generate_move(self, n):

        i = random.randint(0, n - 3)
        j = random.randint(i + 2, n - 1)

        return i, j

    # =========================================================
    # cooling schedule
    # =========================================================
    def cooling(self, t):
        return t * 0.95

    # =========================================================
    # main solver
    # =========================================================
    def solve(self, instance: np.ndarray) -> dict:

        n = instance.shape[0]
        adj = instance

        greedy = NonDeterministicGreedyStrategy()
        solution = greedy.solve(instance)

        current_path = solution["path"]
        current_cost = solution["distance"]

        best_path = current_path.copy()
        best_cost = current_cost

        temperature = 100.0

        while temperature > 1e-4:

            for _ in range(n * 10):

                i, j = self.generate_move(n)

                delta = self.compute_delta(current_path, i, j, adj)

                # =================================================
                # Acceptance rule
                # =================================================
                if delta < 0:
                    accept = True
                else:
                    try:
                        prob = math.exp(-delta / temperature)
                    except OverflowError:
                        prob = 0.0

                    accept = random.random() < prob

                if not accept:
                    continue

                # =================================================
                # Apply 2-opt move
                # =================================================
                current_path = (
                    current_path[:i + 1]
                    + current_path[i + 1:j + 1][::-1]
                    + current_path[j + 1:]
                )

                current_cost += delta

                # =================================================
                # Update best
                # =================================================
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_path = current_path.copy()

            temperature = self.cooling(temperature)

        return {
            "distance": best_cost,
            "path": best_path
        }