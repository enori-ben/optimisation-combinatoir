import numpy as np
import heapq
import random
from tsp.tsp_strategy import Strategy


class NonDeterministicGreedyStrategy(Strategy):

    # =========================================================
    # Solve TSP (stochastic greedy)
    # =========================================================
    def solve(self, instance: np.ndarray) -> dict:

        n = instance.shape[0]
        adj = instance

        visited = set()

        # random start improves diversity
        current = random.randint(0, n - 1)

        visited.add(current)
        path = [current]

        total = 0.0

        while len(visited) < n:

            candidates = []

            for j in range(n):
                if j not in visited:
                    candidates.append((adj[current, j], j))

            # take top-k best candidates
            k = min(3, len(candidates))
            best_k = heapq.nsmallest(k, candidates)

            # stochastic selection among best-k
            cost, next_city = random.choice(best_k)

            total += cost
            visited.add(next_city)
            path.append(next_city)

            current = next_city

        # close tour
        total += adj[path[-1], path[0]]
        path.append(path[0])

        return {
            "distance": total,
            "path": path
        }