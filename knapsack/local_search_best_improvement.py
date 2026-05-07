import numpy as np
import itertools
from knapsack.knapsack_strategy import Strategy
from knapsack.nondeterministic_greedy import NonDeterministicGreedyStrategy

class LocalSearchBestImprovement(Strategy):
    
    def generateAllFeasibleSolutions(self, instance, solution):
        """
        Generate all feasible neighboring solutions by exploring move types.
        Each neighbor is represented as a move tuple (drop_idxs, add_idxs),
        encoding only the *change* (not the full solution vector), so that
        the actual decision array is reconstructed lazily when needed.
        """

        c_decision = solution["decision"]
        W_cap = instance["capacity"]
        weights = instance["weights"]
        profits = instance["profits"]
        
        inside_items = np.where(c_decision == 1)[0]
        outside_items = np.where(c_decision == 0)[0]

        # Pregenerate combinations
        outside_pairs = list(itertools.combinations(outside_items, 2))
        inside_pairs = list(itertools.combinations(inside_items, 2))
        
        feasibleNeighbors = []

        # Helper
        def add_neighbor(drop_idxs, add_idxs):
            w_delta = sum(weights[j] for j in add_idxs) - sum(weights[i] for i in drop_idxs)

            # feasibility check
            if solution["weight"] + w_delta <= W_cap:
                p_delta = sum(profits[j] for j in add_idxs) - sum(profits[i] for i in drop_idxs)
                
                
                feasibleNeighbors.append({
                    "profit": solution["profit"] + p_delta,
                    "weight": solution["weight"] + w_delta,

                    # encode the neighbor by a move, the caller should reconstruct the neighbor,
                    # which is more efficient
                    "move": (drop_idxs, add_idxs) 
                })

        # generate up to 100000 neighbor
        counter = 0
        # 1-in / 1-out
        for i in inside_items:
            for j in outside_items:
                add_neighbor([i], [j])
                counter += 1
            
            if counter > 20000:
                break

        # 1-out / 2-in
        for i in inside_items:
            for j1, j2 in outside_pairs:
                add_neighbor([i], [j1, j2])
                counter += 1
            
            if counter > 45000: 
                break

        # 2-out / 1-in
        for i1, i2 in inside_pairs:
            for j in outside_items:
                add_neighbor([i1, i2], [j])
                counter += 1
            
            if counter > 75000:
                break

        # 2-out / 2-in
        for i1, i2 in inside_pairs:
            for j1, j2 in outside_pairs:
                add_neighbor([i1, i2], [j1, j2])
                counter += 1
            
            if counter > 100000:
                break

        return feasibleNeighbors


    def solve(self, instance: dict) -> dict:

        W = instance["capacity"]

        nondeterministic_greedy = NonDeterministicGreedyStrategy()

        solution = nondeterministic_greedy.solve(instance)

        improved = True
        while improved:
            
            improved = False

            feasibleNeighbors = self.generateAllFeasibleSolutions(instance, solution)

            if not feasibleNeighbors:
                break

            best_neighbor = feasibleNeighbors[0]

            for neighbor in feasibleNeighbors[1:]:
                if neighbor["profit"] > best_neighbor["profit"]:
                    best_neighbor = neighbor

            if solution["profit"] < best_neighbor["profit"]:

                for drop_idx in best_neighbor["move"][0]:
                    solution["decision"][drop_idx] = 0

                for add_idx in best_neighbor["move"][1]:
                    solution["decision"][add_idx] = 1
                
                solution["profit"] = best_neighbor["profit"]
                solution["weight"] = best_neighbor["weight"]

                improved = True
                    


        return {
            "profit": solution["profit"],
            "weight": solution["weight"],
            "decision": solution["decision"]
        }
                



                


# for i in range(n_items):

            #     if current_decision[i] != 1:
            #         continue

            #     for j in range(n_items):

            #         if j == i or current_decision[j] != 0:
            #             continue

            #         n_weight = current_weight - instance["weights"][i] + instance["weights"][j]
            #         n_profit = current_profit - instance["profits"][i] + instance["profits"][j]

            #         if n_weight <= W and n_profit > best_profit:

            #             best_move = (i, j)

            #             best_weight = n_weight
            #             best_profit = n_profit

            #             improved = True
            
            # if improved:

            #     current_decision[best_move[0]] = 0
            #     current_decision[best_move[1]] = 1

            #     current_profit = best_profit
            #     current_weight = best_weight
                


