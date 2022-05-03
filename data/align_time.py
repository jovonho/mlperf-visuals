import os
import pathlib
import numpy as np

# Obtained from previous analysis (see align_time_README.md)
REF_TIMESTAMP = 75530751851216
REF_LOCALTIME = np.datetime64("2022-04-29T14:29:33.000000000")

TRACE_DIR = "trace_4gpus_1xRAM/"
OUTPUT_DIR = "ta_4gpus_1xRAM/"

def main():
    ref_ts = REF_TIMESTAMP
    # Add 5h to convert from EST to UTC
    ref_t = REF_LOCALTIME + np.timedelta64(5, "h")

    traces = ["openat", "close", "read", "write", "mmap", "create_del", "bio"]

    pathlib.Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    for trace in traces:

        print(f"Processing {trace}")

        infile = open(os.path.join(TRACE_DIR, "trace_" + trace + ".out"), "r")
        outfile = open(os.path.join(OUTPUT_DIR, trace + "_time_aligned.out"), "w")

        # Discard the first 2 lines of traces
        for _ in range(2):
            infile.readline()

        # Discard 3 more lines for mmap trace
        if trace == "mmap":
            for _ in range(3):
                infile.readline()

        # Discard 5 more lines for create_del trace
        if trace == "create_del":
            for _ in range(5):
                infile.readline()
        
        try:
            for line in infile:
                cols = " ".join(line.split()).split(" ")
                # Handle empty lines
                if cols[0] == "":
                    continue
                # Get the timestamp
                ts = int(cols[0])
                # Calculate the diff
                ts_delta = ts - ref_ts
                # Get the UTC time
                t = ref_t + ts_delta
                outfile.write(np.datetime_as_string(t) + " " + " ".join(cols[1::]) + "\n")
        except Exception as e:
            print(f"Error while processing trace_{trace}")
            print(e)
            continue

if __name__ == "__main__":
    main()
