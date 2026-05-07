import numpy as np
import itertools
from knapsack.knapsack_strategy import Strategy
from knapsack.nondeterministic_greedy import NonDeterministicGreedyStrategy

class LocalSearchFirstImprovement(Strategy):
    
    def generateNeighbors(self, instance, solution):
        """
        Generate feasible neighboring solutions by exploring move types.
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

        outside_pairs = list(itertools.combinations(outside_items, 2))
        inside_pairs = list(itertools.combinations(inside_items, 2))

        # Helper 
        def get_move(drop_idxs, add_idxs):
            w_delta = sum(weights[j] for j in add_idxs) - sum(weights[i] for i in drop_idxs)

            # feasibility check
            if solution["weight"] + w_delta <= W_cap:
                p_delta = sum(profits[j] for j in add_idxs) - sum(profits[i] for i in drop_idxs)

                # return the solution
                return {

                    "profit": solution["profit"] + p_delta,
                    "weight": solution["weight"] + w_delta,

                    # encode the neighbor by a move, the caller should reconstruct the neighbor,
                    # which is more efficient
                    "move": (drop_idxs, add_idxs)
                }
            return None

        # 1-out / 1-in
        for i in inside_items:
            for j in outside_items:
                move = get_move([i], [j])
                if move:
                    # yield is the as return 
                    yield move

        # 1-out / 2-in
        for i in inside_items:
            for pair in outside_pairs:
                move = get_move([i], pair)
                if move:
                    # yield is the as return
                    yield move

        # 2-out / 1-in
        for pair in inside_pairs:
            for j in outside_items:
                move = get_move(pair, [j])
                if move:
                    # yield is the as return 
                    yield move

        # 2-out / 2-out
        for p_in in inside_pairs:
            for p_out in outside_pairs:
                move = get_move(p_in, p_out)
                if move: 
                    # yield is the as return
                    yield move


    def solve(self, instance: dict) -> dict:

        W = instance["capacity"]

        nondeterministic_greedy = NonDeterministicGreedyStrategy()

        solution = nondeterministic_greedy.solve(instance)

        while True:
            found_improvement = False
            
            i = 0

            # Iterate through the generator, the generator will return the next neighbor upon request
            for neighbor in self.generateNeighbors(instance, solution):

                # see up to 100000 neighbor
                if i > 99999:
                    break

                if neighbor["profit"] > solution["profit"]:

                    # improvement found
                    drops, adds = neighbor["move"]

                    for idx in drops: 
                        solution["decision"][idx] = 0

                    for idx in adds:  
                        solution["decision"][idx] = 1
                    
                    solution["profit"] = neighbor["profit"]
                    solution["weight"] = neighbor["weight"]
                    
                    found_improvement = True
                    break

                i += 1
            
            if not found_improvement:

                # local optimum is reached
                break 
                
        
        return {
            "profit": solution["profit"],
            "weight": solution["weight"],
            "decision": solution["decision"],
        }
             