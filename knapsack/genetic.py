import random
import numpy as np

from knapsack.knapsack_strategy import Strategy
from knapsack.nondeterministic_greedy import NonDeterministicGreedyStrategy


class GeneticStrategy(Strategy):

    POPULATION_SIZE = 100
    MAX_ITERATIONS = 100
    MUTATION_RATE = 0.01

    # =========================================================
    # Selection
    # =========================================================
    def select_operator(self, population):
        """
        Tournament selection.
        Keeps 50% of the population.
        """
        selected = []
        target_size = len(population) // 2

        for _ in range(target_size):

            # Randomly choose 2 individuals
            i, j = np.random.choice(len(population), size=2, replace=False)

            candidate_1 = population[i]
            candidate_2 = population[j]

            # Keep the one with the higher profit
            winner = (
                candidate_1
                if candidate_1["profit"] > candidate_2["profit"]
                else candidate_2
            )

            selected.append(winner)

        return selected

    # =========================================================
    # Repair Function
    # =========================================================
    def repair_solution(self, solution, weights, profits, capacity):
        """
        Repairs an infeasible knapsack solution
        using a Greedy Drop Heuristic.
        """

        current_weight = sum(
            weights[i]
            for i, gene in enumerate(solution)
            if gene == 1
        )

        # Already feasible
        if current_weight <= capacity:
            return solution

        # Get included items
        included_items = [
            i for i, gene in enumerate(solution)
            if gene == 1
        ]

        # Sort by value/weight ratio (worst first)
        included_items.sort(
            key=lambda i: profits[i] / weights[i]
        )

        # Remove worst items until feasible
        for idx in included_items:

            if current_weight <= capacity:
                break

            solution[idx] = 0
            current_weight -= weights[idx]

        return solution

    # =========================================================
    # Crossover
    # =========================================================
    def crossover(self, instance, selected_population):
        """
        Single-point crossover.
        """

        children = []

        shuffled_indices = list(range(len(selected_population)))
        np.random.shuffle(shuffled_indices)

        weights = instance["weights"]
        profits = instance["profits"]
        capacity = instance["capacity"]

        for idx in range(0, len(shuffled_indices) - 1, 2):

            parent_1 = selected_population[
                shuffled_indices[idx]
            ]["decision"]

            parent_2 = selected_population[
                shuffled_indices[idx + 1]
            ]["decision"]

            chromosome_length = len(parent_1)

            # Random crossover point
            cut_point = np.random.randint(1, chromosome_length)

            # Create children
            child_1 = np.concatenate((
                parent_1[:cut_point],
                parent_2[cut_point:]
            ))

            child_2 = np.concatenate((
                parent_2[:cut_point],
                parent_1[cut_point:]
            ))

            # Repair infeasible children
            child_1 = self.repair_solution(
                child_1,
                weights,
                profits,
                capacity
            )

            child_2 = self.repair_solution(
                child_2,
                weights,
                profits,
                capacity
            )

            children.extend([child_1, child_2])

        return children

    # =========================================================
    # Mutation
    # =========================================================
    def mutate(self, children, mutation_rate,
               weights, profits, capacity):
        """
        Applies bit-flip mutation.
        """

        mutated_population = []

        for solution in children:

            mutated = False

            for gene_index in range(len(solution)):

                if random.random() < mutation_rate:

                    # Flip bit
                    solution[gene_index] = (
                        1 - solution[gene_index]
                    )

                    mutated = True

            # Repair only if mutation occurred
            if mutated:
                solution = self.repair_solution(
                    solution,
                    weights,
                    profits,
                    capacity
                )

            mutated_population.append(solution)

        return mutated_population

    # =========================================================
    # Formatting
    # =========================================================
    def format_population(self, population, weights, profits):
        """
        Converts binary solutions into dictionaries
        containing:
            - profit
            - weight
            - decision vector
        """

        formatted_population = []

        for solution in population:

            total_profit = sum(
                profits[i]
                for i, gene in enumerate(solution)
                if gene == 1
            )

            total_weight = sum(
                weights[i]
                for i, gene in enumerate(solution)
                if gene == 1
            )

            formatted_population.append({
                "profit": total_profit,
                "weight": total_weight,
                "decision": list(solution)
            })

        return formatted_population

    # =========================================================
    # Initial Population
    # =========================================================
    def generate_initial_population(self, instance):
        """
        Generates the initial population
        using a non-deterministic greedy strategy.
        """

        population = []

        for _ in range(self.POPULATION_SIZE):

            strategy = NonDeterministicGreedyStrategy()
            solution = strategy.solve(instance)

            population.append(solution)

        return population

    # =========================================================
    # Main Solver
    # =========================================================
    def solve(self, instance):
        """
        Solves the knapsack problem
        using a Genetic Algorithm.
        """

        weights = instance["weights"]
        profits = instance["profits"]
        capacity = instance["capacity"]

        # Generate initial population
        population = self.generate_initial_population(instance)

        # Evolution loop
        for _ in range(self.MAX_ITERATIONS):

            # Selection
            selected_population = self.select_operator(population)

            # Crossover
            children = self.crossover(
                instance,
                selected_population
            )

            # Mutation
            children = self.mutate(
                children,
                self.MUTATION_RATE,
                weights,
                profits,
                capacity
            )

            # Convert children to dictionary format
            children = self.format_population(
                children,
                weights,
                profits
            )

            # Merge populations
            population = selected_population + children

            # Sort by profit (descending)
            population.sort(
                key=lambda individual: individual["profit"],
                reverse=True
            )

            # Keep best individuals only
            population = population[:self.POPULATION_SIZE]

        # Return best solution
        return max(
            population,
            key=lambda individual: individual["profit"]
        )