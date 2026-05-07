import numpy as np
from knapsack.knapsack_strategy import Strategy


class NonDeterministicGreedyStrategy(Strategy):

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


        n = sorted_indices.shape[0]
        while w <= W and n > 0:
            if n >= 3:
                # Choose between 0, 1, or 2
                choice = np.random.randint(0, 3) 

            # treat the case where we have only 2 items
            elif n == 2:
                # Choose between 0 or 1
                choice = np.random.randint(0, 2)
            
            # treat the case where we have only 1 item
            else:
                choice = 0
            
            # check if we can add the item to the solution
            if w + weights[sorted_indices[choice]] <= W:

                # update the decision bit array
                decision_array[sorted_indices[choice]] = 1
                w += weights[sorted_indices[choice]]
            
            # delete the item once chosen
            sorted_indices = np.delete(sorted_indices, choice)
            n -= 1

        # Final profit calculation using the decision mask
        max_profit = np.dot(profits, decision_array)

        return {
            "profit": max_profit,
            "weight": w,
            "decision": decision_array
        }