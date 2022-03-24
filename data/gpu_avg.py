from itertools import zip_longest as izip_longest
from statistics import mean
import numpy as np


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)


def main():
    infile = open("data/gpu_data/gpu.raw", "r")
    outcsv = open("data/gpu_data/gpu_avg.csv", "w")

    # Print headers
    headers = ["timestamp", "sm", "mem", "fb"]
    outcsv.write(",".join(headers) + "\n")

    # Read the file 8 by 8, compute the average for all columns and write out
    for line_batch in grouper(infile, 8):

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
    main()
