import numpy as np
from tsp.tsp_strategy import Strategy


class DeterministicGreedyStrategy(Strategy):

    def solve(self, instance: np.ndarray) -> dict:

        # Initilize the number of cities
        num_of_cities = instance.shape[1]

        # the graph of cities modeled as an adjancency matrix
        adj_matrix = instance

        # Initiaze the set of visited cities, which is empty at the beginnig
        visited = set()

        # path taken to make a tour, which empty at the beginnig
        path = []

        # Start from city 0 and mark it as visited, 
        # and initialize the number of visited cities to 1.
        # Also, because it is the starting point, add to the path list
        current_city = 0
        visited.add(0)
        path.append(0)

        total_distance = 0

        # While we haven't visited all cities
        while len(visited) < num_of_cities:
            
            i = current_city

            # find the nearest unvisited city
            best = min(
                (adj_matrix[i, j], (i, j))
                for j in range(num_of_cities)
                if j not in visited
            )

            # update the distance 
            total_distance += best[0]

            # mark the new city as visited
            visited.add(best[1][1])

            # mark the new city as the current city
            current_city = best[1][1]

            # append it to the path
            path.append(best[1][1])

        # close the tour and update the total distance
        total_distance += adj_matrix[0, path[-1]]
        path.append(0) 

        return {"distance" : total_distance, "path" : path}