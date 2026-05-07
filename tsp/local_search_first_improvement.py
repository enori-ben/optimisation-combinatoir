import numpy as np
from tsp.tsp_strategy import Strategy
from tsp.nondeterministic_greedy import NonDeterministicGreedyStrategy

class LocalSearchFirstImprovement(Strategy):
    
    # Helper function used to compute the change if we swap the edges (i, i+1) and (j, j+1)
    def compute_change(self, path, i, j, adj_matrix):
        
        edge1 = (path[i], path[i+1])
        edge2 = (path[j], path[j+1])

        # calculate the change
        change = (adj_matrix[edge1[0], edge2[0]] + adj_matrix[edge1[1], edge2[1]]) \
                - (adj_matrix[edge1[0], edge1[1]] + adj_matrix[edge2[0], edge2[1]])
        
        return change

    def make_an_improvement(self, n, path, adj_matrix):
        count = 0

        # visit at maximum 10000 neighbors, otherwise it would take very long time
        max_neighbors = 10000

        for i in range(n - 2):
            for j in range(i + 2, n):

                # Skip adjacent edges
                if (j + 1) % n == i:
                    continue
                
                # Increment and check the budget
                count += 1
                if count > max_neighbors:

                    # No better solution found in the 1st 10000 neighbors
                    return {"change": 0, "edges": None}

                change = self.compute_change(path, i, j, adj_matrix)
                
                # check is the change is negative, which implies an improvement is found
                if change < 0:
                    return {"change": change, "edges": (i, j)}

        # No better solution found
        return {"change": 0, "edges": None}
                

    def solve(self, instance: np.ndarray) -> dict:

        # Initilize the number of cities
        num_of_cities = instance.shape[1]

        # the graph of cities modeled as an adjancency matrix
        adj_matrix = instance
        
        # get a random initial solution using a nondetermistic greedy approach
        nondeterminitic_greedy = NonDeterministicGreedyStrategy()
        initial_solution = nondeterminitic_greedy.solve(instance)

        # Assume the initial solution is the best one
        current_local_optimum_cost = initial_solution["distance"]
        path = initial_solution["path"]


        improved = True

        # while there is an improvement
        while improved:
            
            # iterate the neighbors and stop on the first neighbor with a shorter distance
            result =  self.make_an_improvement(num_of_cities, path, adj_matrix)

            if result["change"] < 0:

                # update optimal distance
                current_local_optimum_cost += result["change"]

                edges_to_swap = result["edges"]

                i = edges_to_swap[0]
                j = edges_to_swap[1]

                # update path
                new_path = path[:i+1] + path[j:i:-1] + path[j+1:]
                path = new_path

                # jump to the while loop directly
                continue

            # There is no improvement
            improved = False
        
        return {"distance" : current_local_optimum_cost, "path" : path}