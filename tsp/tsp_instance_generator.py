from tsp.tsp_parser import parser
import os
import numpy as np

tsp_path = './tsplib-master'

number_of_skipped = 0
number_of_intances = 0

def tsp_iterator(folder_path=tsp_path):

    for tsp_file in os.listdir(folder_path):

        full_path = os.path.join(folder_path, tsp_file)

        with open(full_path, 'r') as tsp_content:
            content = tsp_content.read()

        print(full_path)
        global number_of_intances
        global number_of_skipped
        number_of_intances += 1
        try:
            tsp_instance = parser.parse(content)

            if tsp_instance is None:
                print(f"Skipping {tsp_file} due to syntax error.")
                global number_of_skipped
                number_of_skipped += 1
                continue

            yield tsp_instance

        except ValueError as e:
            print(f"Skipping {tsp_file}: {e}")
            number_of_skipped += 1
            continue


instances = tsp_iterator()



output_dir = "adj_matrices"
os.makedirs(output_dir, exist_ok=True)

for i, instance in enumerate(instances):
    filename = os.path.join(output_dir, f"{instance['name']}.csv")
        
    # Save the matrix
    np.savetxt(filename, instance['adj_mat'], delimiter=",", fmt="%.6f")
    print(f"Saved: {filename}")


