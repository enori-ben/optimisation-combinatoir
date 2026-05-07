import numpy as np
from tsp.tsp_strategy import Strategy
from tsp.nondeterministic_greedy import NonDeterministicGreedyStrategy

class LocalSearchBestImprovement(Strategy):
    
    # Helper function used to compute the change if we swap the edges (i, i+1) and (j, j+1)
    def compute_change(self, path, i, j, adj_matrix):
        
        # the 1st edge
        edge1 = (path[i], path[i+1])

        # the 2nd edge
        edge2 = (path[j], path[j+1])

        # compute the change
        change = (adj_matrix[edge1[0], edge2[0]] + adj_matrix[edge1[1], edge2[1]]) \
                - (adj_matrix[edge1[0], edge1[1]] + adj_matrix[edge2[0], edge2[1]])
        
        return change
                

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

            improved = False
            best_change = 0
            edges_to_swap = None
            
            count = 0
            max_neighbors = 10000
            
            # Use a labeled break or nested loop control
            stop_searching = False

            for i in range(num_of_cities - 2):
                for j in range(i + 2, num_of_cities):
                    if (j + 1) % num_of_cities != i:
                        
                        count += 1
                        if count > max_neighbors:
                            stop_searching = True
                            break
                        
                        # Compute the change if we swap the edges (i, i+1) and (j, j+1)
                        change = self.compute_change(path, i, j, adj_matrix)
                        
                        # Keep track of the best one we've seen in this window
                        if change < best_change:
                            best_change = change
                            edges_to_swap = (i, j)
                
                if stop_searching:
                    break
            
            # Check if the best change is negative, which means there is an improved solution
            if best_change < 0:

                # There is an improvement
                improved = True

                current_local_optimum_cost += best_change
                i = edges_to_swap[0]
                j = edges_to_swap[1]

                # update path
                new_path = path[:i+1] + path[j:i:-1] + path[j+1:]
                path = new_path
        

        # return the best solution
        return {"distance" : current_local_optimum_cost, "path" : path}