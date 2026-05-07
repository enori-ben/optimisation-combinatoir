import numpy as np
from knapsack.knapsack_strategy import Strategy


class DeterministicGreedyStrategy(Strategy):

    def solve(self, instance: dict) -> dict:
        
        # get the number of items
        n_items = instance["profits"].shape[0]
        
        # extract the list of profits and weights, as well as the maximum capacity of the bag
        profits = instance["profits"]
        weights = instance["weights"]
        W = instance["capacity"]
        
        # Calculate ratios and sort the array in descending order, then return the list of indices
        ratios = profits / weights
        sorted_indices = np.argsort(-ratios)


        # initialize the current weight of the bag by zero
        w = 0

        # initialize the decision bit array by zeros, since no item is chosen yet
        decision_array = np.zeros(n_items)

        # pick items greedly
        for idx in sorted_indices:
            if w + weights[idx] <= W:

                # update the decision bit
                decision_array[idx] = 1
                w += weights[idx]

        # Final profit calculation using the decision mask (simple dot product will do the job)
        max_profit = np.dot(profits, decision_array)

        # return the solution
        return {
            "profit": max_profit,
            "weight": w,
            "decision": decision_array
        }







        

