import numpy as np
import random
import math
from knapsack.knapsack_strategy import Strategy
from knapsack.nondeterministic_greedy import NonDeterministicGreedyStrategy

class SimulatedAnnealing(Strategy):

    def get_feasible_random_neighbor(self, instance, solution):

        W_cap = instance["capacity"]
        weights = instance["weights"]
        profits = instance["profits"]
        
        inside = list(np.where(solution["decision"] == 1)[0])
        outside = list(np.where(solution["decision"] == 0)[0])

        # Try up to 50 times to find a feasible move; if not, return None
        for _ in range(50):

            # Randomly pick a move type
            move_type = random.choices(['1-1', '1-2', '2-1', '2-2'], weights=[40, 30, 20, 10])[0]
            
            
            try:
                if move_type == '1-1':
                    drops, adds = random.sample(inside, 1), random.sample(outside, 1)
                elif move_type == '1-2':
                    drops, adds = random.sample(inside, 1), random.sample(outside, 2)
                elif move_type == '2-1':
                    drops, adds = random.sample(inside, 2), random.sample(outside, 1)
                else: 
                    drops, adds = random.sample(inside, 2), random.sample(outside, 2)
            except ValueError: 
                continue

            # Calculate weight delta
            w_delta = sum(weights[j] for j in adds) - sum(weights[i] for i in drops)
            
            # Feasibility Check
            if solution["weight"] + w_delta <= W_cap:
                p_delta = sum(profits[j] for j in adds) - sum(profits[i] for i in drops)
                
                return {
                    "p_delta": p_delta,
                    "w_delta": w_delta,
                    "move": (drops, adds)
                }
                
        return None 



    def cooling(self, temperature):
        return temperature * 0.95

    def solve(self, instance: dict) -> dict:

        n_items = instance["profits"].shape[0]
        W = instance["capacity"]

        # generate an initial solution
        nondeterministic_greedy = NonDeterministicGreedyStrategy()
        solution = nondeterministic_greedy.solve(instance)

        # initialize the temperature
        temperature = 100.0

        best_so_far = solution.copy()

        while temperature >= 1e-4:
            for _ in range(n_items * 10):
                
                neighbor = self.get_feasible_random_neighbor(instance, solution)

                if neighbor is None:
                    continue
                

                # extract the profit change
                change = neighbor["p_delta"]
                
                # Acceptance Logic
                accepted = False
                if change > 0:
                    accepted = True
                else:
                    # when change is negative
                    if random.random() < math.exp(change / temperature):
                        accepted = True
                
                if accepted:
                    
                    # update the current solution
                    drops, adds = neighbor["move"]

                    for idx in drops: 
                        solution["decision"][idx] = 0

                    for idx in adds:  
                        solution["decision"][idx] = 1
                    
                    solution["profit"] += neighbor["p_delta"]
                    solution["weight"] += neighbor["w_delta"]

                    if solution["profit"] > best_so_far["profit"]:
                        best_so_far = {
                            "profit": solution["profit"],
                            "weight": solution["weight"],
                            "decision": solution["decision"].copy() 
                        }
            
            # cool the temperature
            temperature = self.cooling(temperature)

        return {
            "profit": best_so_far["profit"],
            "weight": best_so_far["weight"],
            "decision": best_so_far["decision"],
        }