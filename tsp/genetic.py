import numpy as np
from tsp.tsp_strategy import Strategy
from tsp.nondeterministic_greedy import NonDeterministicGreedyStrategy


class GeneticStrategy(Strategy):

    # The select operator
    def selectOperator(self, solutions):
        """
        Tournament selection: keeps 50% of the population.
        """
        selected = []

        # target is to select 50% of the population
        target = len(solutions) // 2

        for _ in range(target):
            i, j = np.random.choice(len(solutions), size=2, replace=False)
            d_i = solutions[i]["distance"]
            d_j = solutions[j]["distance"]

            # Select the one with shortest distance
            winner = solutions[i] if d_i < d_j else solutions[j]
            selected.append(winner)

        # return the selected cities
        return selected

    # Crossover Operator
    def crossover(self, solutions):
        """
        Simple Ordered Crossover (OX) with a single cut-point (split into 2 segments).
        """
        children = []

        # Helper inner-function used to perform the crossing
        def ox(parent_a, parent_b, cut):
            """Simple Order Crossover."""

            # Get the first 'cut' cities directly from Parent A.
            segment = parent_a[:cut]
            in_segment = set(segment)


            # Collect cities from Parent B that are NOT in the segment.
            # We start from the 'cut' index to the end to maintain relative 
            # order starting from the point of the break (circular logic).
            tail = [city for city in parent_b[cut:] if city not in in_segment]
            tail += [city for city in parent_b[:cut] if city not in in_segment]

            return segment + tail

        # get the list incdices
        indices = list(range(len(solutions)))

        # shuffle the indices and then create the couples
        np.random.shuffle(indices)

        # make couples then crossover
        for idx in range(0, len(indices) - 1, 2):

            # the first individual of the couple (idx, idx+1)
            p1 = solutions[indices[idx]]["path"]

            # the second individual of the couple (idx, idx+1)
            p2 = solutions[indices[idx + 1]]["path"]

            # Starting city
            depot = p1[0] 

            # Strip depot from both ends since the starting city is always the same
            p1_inner = p1[1:-1]
            p2_inner = p2[1:-1]
            n = len(p1_inner)

            # Random cut point inside the interior
            k = np.random.randint(1, n - 1)

            # first child
            child1_inner = ox(p1_inner, p2_inner, k)

            # second child
            child2_inner = ox(p2_inner, p1_inner, k)

            # Re-attach the starting city to the children
            children.append([depot] + child1_inner + [depot])
            children.append([depot] + child2_inner + [depot])

        # return the newly generated individuals (children)
        return children

    def mutate(self, children, mutation_rate=0.05):
        """
        Swap mutation
        """
        mutated = []
        for path in children:
            path = list(path)
            if np.random.random() < mutation_rate:
                
                # Randomly chose 2 cities to swap
                i, j = np.random.choice(range(1, len(path) - 1), size=2, replace=False)

                # Swap two cities (pythonic way)
                path[i], path[j] = path[j], path[i]

            mutated.append(path)

        return mutated

    def _path_to_solution(self, path, instance):
        """
        Compute the total distance of a closed path and return a solution dictionary object.
        """
        total = 0.0
        for i in range(len(path) - 1):
            total += instance[path[i]][path[i + 1]]
        return {"distance": total, "path": path}

    def best_path(self, solutions):
        """Return the solution dict with the smallest distance."""
        return min(solutions, key=lambda s: s["distance"])


    
    def solve(self, instance: np.ndarray) -> dict:

        MAX_ITERATION = 1000

        # Generate initial population ONCE before the loop (500 individuals) using greedy algorithm
        solutions = []

        nondeterministic_greedy = NonDeterministicGreedyStrategy()
        # repeat 500 times
        for _ in range(500):
            solution = nondeterministic_greedy.solve(instance)
            solutions.append(solution)

        # Assume the current best solution has an infinite distance, then update once a better solution found
        current_best = {"distance": np.inf, "path": None}
        best = current_best

        # Evolve the population across iterations, iterate 1000 times
        for _ in range(MAX_ITERATION):

            # Selection (keep 50% of the population using Tounrnament strategy)
            selected = self.selectOperator(solutions)

            # Crossover
            child_paths = self.crossover(selected)

            # Perturb ~5% of children (mutation)
            child_paths = self.mutate(child_paths, 0.05)

            # Convert child paths to solution dictionaries
            children = [self._path_to_solution(p, instance) for p in child_paths]

            # Merge selected parents + children
            combined = selected + children
            combined.sort(key=lambda s: s["distance"])

            # keep only 1000 individual (keep the fittest).
            solutions = combined[:1000]

            # get the best path from the current population
            current_best = self.best_path(solutions)

            # update the best path is the current_best is better
            if current_best['distance'] < best['distance']:
                best = current_best

        # return the best path
        return {"distance": best["distance"], "path": best["path"]}