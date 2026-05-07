import numpy as np
from tsp.tsp_strategy import Strategy
from tsp.nondeterministic_greedy import NonDeterministicGreedyStrategy


class LocalSearchBestImprovement(Strategy):

    # =========================================================
    # Compute 2-opt delta
    # =========================================================
    def compute_change(self, path, i, j, adj):

        a, b = path[i], path[i + 1]
        c, d = path[j], path[j + 1]

        # removed edges
        removed = adj[a, b] + adj[c, d]

        # added edges
        added = adj[a, c] + adj[b, d]

        return added - removed

    # =========================================================
    # Solve (2-opt Best Improvement)
    # =========================================================
    def solve(self, instance: np.ndarray) -> dict:

        n = instance.shape[0]
        adj = instance

        greedy = NonDeterministicGreedyStrategy()
        solution = greedy.solve(instance)

        path = solution["path"]
        best_cost = solution["distance"]

        improved = True

        while improved:

            improved = False
            best_delta = 0
            best_move = None

            # =================================================
            # Search best 2-opt move
            # =================================================
            for i in range(n - 1):
                for j in range(i + 2, n - (0 if i > 0 else 1)):

                    delta = self.compute_change(path, i, j, adj)

                    if delta < best_delta:
                        best_delta = delta
                        best_move = (i, j)

            # =================================================
            # Apply best move
            # =================================================
            if best_move is not None:

                i, j = best_move

                path = (
                    path[:i + 1]
                    + path[i + 1:j + 1][::-1]
                    + path[j + 1:]
                )

                best_cost += best_delta
                improved = True

        return {
            "distance": best_cost,
            "path": path
        }