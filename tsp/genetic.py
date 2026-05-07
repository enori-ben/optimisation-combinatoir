import numpy as np
from tsp.tsp_strategy import Strategy
from tsp.nondeterministic_greedy import NonDeterministicGreedyStrategy


class GeneticStrategy(Strategy):

    # =========================================================
    # Selection (Tournament)
    # =========================================================
    def select_operator(self, population):

        selected = []
        target = len(population) // 2

        for _ in range(target):

            i, j = np.random.choice(len(population), size=2, replace=False)

            if population[i]["distance"] < population[j]["distance"]:
                selected.append(population[i])
            else:
                selected.append(population[j])

        return selected

    # =========================================================
    # Ordered Crossover (OX)
    # =========================================================
    def crossover(self, parents):

        children = []

        def ox(p1, p2, cut):

            segment = p1[:cut]
            used = set(segment)

            tail = [c for c in p2 if c not in used]

            return segment + tail

        indices = np.random.permutation(len(parents))

        for i in range(0, len(indices) - 1, 2):

            p1 = parents[indices[i]]["path"][1:-1]
            p2 = parents[indices[i + 1]]["path"][1:-1]

            depot = parents[indices[i]]["path"][0]

            n = len(p1)
            cut = np.random.randint(1, n)

            c1 = ox(p1, p2, cut)
            c2 = ox(p2, p1, cut)

            children.append([depot] + c1 + [depot])
            children.append([depot] + c2 + [depot])

        return children

    # =========================================================
    # Mutation (swap)
    # =========================================================
    def mutate(self, children, rate=0.05):

        for path in children:

            if np.random.rand() < rate:

                i, j = np.random.choice(
                    range(1, len(path) - 1),
                    size=2,
                    replace=False
                )

                path[i], path[j] = path[j], path[i]

        return children

    # =========================================================
    # Convert path -> solution
    # =========================================================
    def path_to_solution(self, path, instance):

        dist = 0.0

        for i in range(len(path) - 1):
            dist += instance[path[i]][path[i + 1]]

        return {
            "distance": dist,
            "path": path
        }

    # =========================================================
    # Solve
    # =========================================================
    def solve(self, instance):

        POP_SIZE = 500
        MAX_ITER = 1000
        ELITE_SIZE = 50

        greedy = NonDeterministicGreedyStrategy()

        population = [
            greedy.solve(instance)
            for _ in range(POP_SIZE)
        ]

        best = min(population, key=lambda x: x["distance"])

        for _ in range(MAX_ITER):

            # -------------------------
            # Selection
            # -------------------------
            parents = self.select_operator(population)

            # -------------------------
            # Crossover
            # -------------------------
            children_paths = self.crossover(parents)

            # -------------------------
            # Mutation
            # -------------------------
            children_paths = self.mutate(children_paths)

            # -------------------------
            # Convert to solutions
            # -------------------------
            children = [
                self.path_to_solution(p, instance)
                for p in children_paths
            ]

            # -------------------------
            # Elitism (IMPORTANT FIX)
            # -------------------------
            elite = sorted(
                population,
                key=lambda x: x["distance"]
            )[:ELITE_SIZE]

            # -------------------------
            # Merge
            # -------------------------
            population = elite + children

            population = sorted(
                population,
                key=lambda x: x["distance"]
            )[:POP_SIZE]

            # Update best
            if population[0]["distance"] < best["distance"]:
                best = population[0]

        return best