import numpy as np
from tsp.tsp_strategy import Strategy


class DeterministicGreedyStrategy(Strategy):

    def solve(self, instance: np.ndarray) -> dict:

        n = instance.shape[0]
        adj = instance

        visited = set()

        # better: allow flexibility in start city
        current = 0

        visited.add(current)
        path = [current]

        total = 0.0

        while len(visited) < n:

            best_cost = float("inf")
            best_city = None

            for j in range(n):

                if j not in visited:

                    cost = adj[current, j]

                    if cost < best_cost:
                        best_cost = cost
                        best_city = j

            # safety check (should never happen)
            if best_city is None:
                break

            total += best_cost
            visited.add(best_city)
            path.append(best_city)

            current = best_city

        # close tour properly
        total += adj[path[-1], path[0]]
        path.append(path[0])

        return {
            "distance": total,
            "path": path
        }