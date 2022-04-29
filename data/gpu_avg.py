import os
import argparse
import numpy as np
from statistics import mean
from itertools import zip_longest as izip_longest

NUM_GPUS = 4

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)


def main(gpu_trace):

    data_dir = os.path.dirname(gpu_trace)

    infile = open(gpu_trace, "r")
    outcsv = open(os.path.join(data_dir, "gpu_avg.csv"), "w")

    # Print headers
    headers = ["timestamp", "sm", "mem", "fb"]
    outcsv.write(",".join(headers) + "\n")

    # Read the file NUM_GPUS x NUM_GPUS lines at a time. 
    # Compute the average for all columns and write out
    for line_batch in grouper(infile, NUM_GPUS):

        # Hold column values we care about
        wcols = []
        sm = []
        mem = []
        fb = []

        for line in line_batch:
            cols = " ".join(line.split()).replace("-", "0").split(" ")
            if cols[2] == "0":
                # Combine cols 0 and 1 into a UTC timestamp
                ts = f"{cols[0][0:4]}-{cols[0][4:6]}-{cols[0][6:8]}T{cols[1]}"
                ts = str(np.datetime64(ts) + np.timedelta64(5, "h"))
                wcols.append(ts)
            # Extract values
            sm.append(int(cols[5]))
            mem.append(int(cols[6]))
            fb.append(int(cols[9]))

        # Calculate means and append to wcols
        wcols.append(str(mean(sm)))
        wcols.append(str(mean(mem)))
        wcols.append(str(mean(fb)))

        outcsv.write(",".join(wcols) + "\n")

    infile.close()
    outcsv.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Calculates the average GPU usage from an nvidia-smi trace. Outputs a CSV file.")
    p.add_argument("gpu_trace", help="The nvidia-smi trace")
    args = p.parse_args()

    if not os.path.isfile(args.gpu_trace):
        print(f"Invalid trace file given")
        exit(-1) 

    main(args.gpu_trace)
