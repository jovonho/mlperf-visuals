import os
import sys

"""
Fixes the integer overflow bug occuring in VFSRW traces
"""


def bugfix(file_to_fix):

    infile = open(file_to_fix, "r")
    outfile = open(file_to_fix + "_fixed", "w")

    for line in infile:
        cols = line.split(" ")
        lat = int(cols[3])

        if lat < 0:
            print(f"Bug found: latency of {lat}")
            fix = str(int(str(bin(lat & 0xFFFFFFFF)), 2))
            print(f"\tConverting to {fix}")
            cols[3] = fix

        outfile.write(" ".join(cols))

    infile.close()
    outfile.close()

    os.replace(file_to_fix + "_fixed", file_to_fix)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} file_to_fix")
        exit(1)

    bugfix(sys.argv[1])
