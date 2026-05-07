import numpy as np

def get_instances():
    
    sizes = [50, 100, 200, 500, 1000, 2000]

    instances = {
        (i+1): {
            "profits": np.random.uniform(low=1, high=10, size=n),
            "weights": np.random.uniform(low=1, high=10, size=n),
            "capacity": (5 * n) / 4
        }
        for i, n in enumerate(sizes)
    }


    return instances