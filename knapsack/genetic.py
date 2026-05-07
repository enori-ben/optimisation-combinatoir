import numpy as np
from knapsack.knapsack_strategy import Strategy
from knapsack.nondeterministic_greedy import NonDeterministicGreedyStrategy
import random

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

            # randomly pick 2 solutions
            i, j = np.random.choice(len(solutions), size=2, replace=False)
            p_i = solutions[i]["profit"]
            p_j = solutions[j]["profit"]
            
            # Select the one with bigger profit
            winner = solutions[i] if p_i > p_j else solutions[j]
            selected.append(winner)
        
        return selected 

    def repair_knapsack(self, solution, weights, values, max_capacity):
        """
        Repairs an infeasible solution using the Greedy Drop Heuristic.
        """
        
        # Calculate current total weight
        current_weight = sum(w for i, w in enumerate(weights) if solution[i] == 1)
        
        # If the knapsack is within limits, no repair needed
        if current_weight <= max_capacity:
            return solution

        # Identify indices of items currently in the knapsack (gene == 1)
        included_indices = [i for i, gene in enumerate(solution) if gene == 1]

        # Sort these indices by value/weight ratio (ascending: worst first)
        included_indices.sort(key=lambda i: values[i] / weights[i])

        # Iteratively remove items until the weight is feasible
        for idx in included_indices:
            if current_weight <= max_capacity:
                break
            
            # Flip the gene from 1 to 0
            solution[idx] = 0
            current_weight -= weights[idx]

        return solution 
    

    def crossover(self, instance, solutions):
        """
        Simple Ordered Crossover (OX) with a single cut-point (split into 2 segments).
        """
        children = []

        indices = list(range(len(solutions)))
        np.random.shuffle(indices)



        def ox(parent_a, parent_b, cut):
            """OX with a single cut point."""
            segment1 = parent_a[:cut]
            segment2 = parent_b[cut:]

            child = np.concatenate((segment1, segment2))

            # Repair the solution if it is not feasible
            child = self.repair_knapsack(child, instance["weights"], \
                                         instance["profits"], instance["capacity"])

            return child


        for idx in range(0, len(indices) - 1, 2):
            p1 = solutions[indices[idx]]["decision"]
            p2 = solutions[indices[idx + 1]]["decision"]

            n = len(p1)

            # Random cut point
            k = np.random.randint(1, n)

            child1 = ox(p1, p2, k)
            child2 = ox(p1, p2, k)

            
            children.append(child1)
            children.append(child2)

        return children

    def mutate(self, children, mutation_rate, weights, values, max_capacity):
        """
        Mutates a batch of children and ensures they remain feasible.
        """
        mutated_population = []

        for solution in children:
            mutated = False
            
            # Gene-level mutation
            for i in range(len(solution)):
                if random.random() < mutation_rate:
                    # Flip bit
                    solution[i] = 1 - solution[i]  
                    mutated = True
            
            # Repair only if a mutation actually occurred 
            # no need to repair if nothing changed)
            if mutated:
                solution = self.repair_knapsack(solution, weights, values, max_capacity)
            
            mutated_population.append(solution)
            
        return mutated_population

    def best_path(self, solutions):
        """Return the solution dict with the smallest distance."""
        return min(solutions, key=lambda s: s["distance"])


    # Helper function just to make the solutions as a list of dictionary objects
    def format_children(self, children, weights, values):
        """
        Transforms a list of binary arrays into a list of dictionaries 
        containing profit, weight, and the decision array.
        """
        formatted_results = []
        
        for decision_array in children:
            # Calculate total profit and weight for the current decision
            current_profit = sum(v for i, v in enumerate(values) if decision_array[i] == 1)
            current_weight = sum(w for i, w in enumerate(weights) if decision_array[i] == 1)
            
            # Create the dictionary object
            obj = {
                "profit": current_profit,
                "weight": current_weight,
                "decision": list(decision_array)  
            }
            
            formatted_results.append(obj)
            
        return formatted_results

    def solve(self, instance: np.ndarray) -> dict:

        MAX_ITERATION = 100

        # Generate initial population
        solutions = []
        for _ in range(100):
            nondeterministic_greedy = NonDeterministicGreedyStrategy()
            solution = nondeterministic_greedy.solve(instance)
            solutions.append(solution)

        # Evolve the population across iterations
        for i in range(MAX_ITERATION):

            # Selection (keep 50% of the population using Tounrnament strategy)
            selected = self.selectOperator(solutions)

            # Crossover
            children = self.crossover(instance, selected)

            # Perturb ~1% of children
            children = self.mutate(children, 0.01, instance["weights"], \
                                   instance["profits"], instance["capacity"])

            children = self.format_children(children, instance["weights"], instance["profits"])

            # Merge selected parents + children
            combined = selected + children
            combined.sort(key=lambda s: s["profit"])

            # keep only 100 individuals
            solutions = combined[:100]
        

        # Find the object where the "profit" key is maximized
        best_solution = max(solutions, key=lambda x: x['profit'])

        return best_solution