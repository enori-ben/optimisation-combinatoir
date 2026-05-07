from tsp.tsp_parser import parser
import os
import numpy as np


tsp_path = "./tsplib-master"


# =========================================================
# TSPLIB ITERATOR
# =========================================================
def tsp_iterator(folder_path=tsp_path):

    skipped = 0
    total = 0

    for file in os.listdir(folder_path):

        if not file.endswith(".tsp"):
            continue

        full_path = os.path.join(folder_path, file)

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            total += 1

            print(f"Parsing: {file}")

            tsp_instance = parser.parse(content)

            if tsp_instance is None:
                print(f"Skipped (parse error): {file}")
                skipped += 1
                continue

            yield tsp_instance

        except ValueError as e:
            print(f"Skipped {file}: {e}")
            skipped += 1

        except Exception as e:
            print(f"Skipped {file} (unexpected error): {e}")
            skipped += 1

    print("\n=== SUMMARY ===")
    print(f"Total parsed: {total}")
    print(f"Skipped: {skipped}")


# =========================================================
# GENERATE DATASET
# =========================================================
output_dir = "adj_matrices"
os.makedirs(output_dir, exist_ok=True)


for i, instance in enumerate(tsp_iterator()):

    name = instance["name"]

    filename = os.path.join(output_dir, f"{name}.csv")

    np.savetxt(
        filename,
        instance["adj_mat"],
        delimiter=",",
        fmt="%.6f"
    )

    print(f"Saved: {filename}")