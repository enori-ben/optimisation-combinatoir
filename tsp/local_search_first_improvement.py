import numpy as np
from tsp.tsp_strategy import Strategy
from tsp.nondeterministic_greedy import NonDeterministicGreedyStrategy


class LocalSearchFirstImprovement(Strategy):

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
    # First improvement search
    # =========================================================
    def first_improvement(self, n, path, adj):

        for i in range(n - 1):
            for j in range(i + 2, n):

                delta = self.compute_delta(path, i, j, adj)

                if delta < 0:
                    return i, j, delta

        return None

    # =========================================================
    # Solve
    # =========================================================
    def solve(self, instance: np.ndarray) -> dict:

        n = instance.shape[0]
        adj = instance

        greedy = NonDeterministicGreedyStrategy()
        solution = greedy.solve(instance)

        path = solution["path"]
        cost = solution["distance"]

        improved = True

        while improved:

            improved = False

            result = self.first_improvement(n, path, adj)

            if result is None:
                break

            i, j, delta = result

            # apply 2-opt move
            path = (
                path[:i + 1]
                + path[i + 1:j + 1][::-1]
                + path[j + 1:]
            )

            cost += delta
            improved = True

        return {
            "distance": cost,
            "path": path
        }