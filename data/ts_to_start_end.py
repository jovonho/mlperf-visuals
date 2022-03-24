import os
import sys
import numpy as np
from pathlib import Path


def main(filename):

    pid = os.path.basename(filename).split("_")[1]

    infile = open(filename, "r")
    outfile = open(f"st_end_data/st_end_data_{pid}", "w")

    for line in infile:
        cols = line.split(",")
        ts_end = np.datetime64(cols[0])
        lat = int(cols[2])
        ts_start = ts_end - lat
        outfile.write(f"{ts_start},{ts_end},{cols[1]}\n")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} filename")
        exit(1)

    Path("st_end_data").mkdir(parents=True, exist_ok=True)

    filename = sys.argv[1]
    main(filename)
