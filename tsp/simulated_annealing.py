import math
import random
import numpy as np
from tsp.tsp_strategy import Strategy
from tsp.nondeterministic_greedy import NonDeterministicGreedyStrategy

class SimulatedAnnealing(Strategy):

    # Helper function used to compute the change if we swap the edges (i, i+1) and (j, j+1)
    def compute_change(self, path, i, j, adj_matrix):
        
        edge1 = (path[i], path[i+1])
        edge2 = (path[j], path[j+1])

        # calculate the change
        change = (adj_matrix[edge1[0], edge2[0]] + adj_matrix[edge1[1], edge2[1]]) \
                - (adj_matrix[edge1[0], edge1[1]] + adj_matrix[edge2[0], edge2[1]])
        
        return change

    # Helper function used to generate a random edge
    def generate_random_edges(self, n):

        i = random.randint(0, n - 3)
        j = random.randint(i + 2, n - 1)
        
        return i, j


    # Cool the temperature
    def cooling(self, temperature):
        return temperature * 0.95

    def solve(self, instance: np.ndarray) -> dict:
        
        # Initilize the number of cities
        num_of_cities = instance.shape[1]

        # the graph of cities modeled as an adjancency matrix
        adj_matrix = instance

        # get a random initial solution using a nondetermistic greedy approach
        nondeterminitic_greedy = NonDeterministicGreedyStrategy()
        initial_solution = nondeterminitic_greedy.solve(instance)

        # The current cost and path
        current_cost = initial_solution["distance"]
        current_path = initial_solution["path"]
        
        # Assume the best cost and path is the current one
        best_cost = current_cost
        best_path = current_path.copy()

        # Set the temprature, for simplicity I initialized it to 100
        temperature = 100
        
        while temperature >= 1e-4:
            
            for _ in range(num_of_cities * 10):

                # generate two random non-adjacent edges
                i, j = self.generate_random_edges(num_of_cities)
                
                # compute the change if we swap the edges (i, i+1) and (j, j+1)
                delta_E = self.compute_change(current_path, i, j, adj_matrix)
                
                # check if the generated solution is better
                if delta_E < 0:
                    
                    # update current cost 
                    current_cost += delta_E

                    # update the current path
                    new_path = current_path[:i+1] + current_path[j:i:-1] + current_path[j+1:]
                    current_path = new_path


                    if best_cost > current_cost:
                        best_cost = current_cost
                        best_path = current_path.copy()
                
                else:
                    # generate a random float between 0 and 1
                    p = random.uniform(0, 1)
                    
                    # calculate the probability of the solution being accepted
                    if p < math.exp( - delta_E / temperature):
                        
                        # update the current cost
                        current_cost += delta_E

                        # update current path
                        new_path = current_path[:i+1] + current_path[j:i:-1] + current_path[j+1:]
                        current_path = new_path

                        if best_cost > current_cost:
                            best_cost = current_cost
                            best_path = current_path.copy()
            
            
            # cool the temperature
            temperature = self.cooling(temperature)
            
        return {"distance" : best_cost, "path" : best_path}