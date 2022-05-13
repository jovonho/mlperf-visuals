import os
import pathlib
import numpy as np
import argparse


def main(traces_dir, output_dir, ref_ts, ref_t):
    # Add 5 hours to convert to UTC (will change based on location)

    ref_t = ref_t + np.timedelta64(5, "h")

    traces = ["openat", "close", "read", "write", "mmap", "create_del", "bio"]

    for trace in traces:

        print(f"Processing {trace}")

        infile = open(os.path.join(traces_dir, "trace_" + trace + ".out"), "r")
        outfile = open(os.path.join(output_dir, trace + "_time_aligned.out"), "w")

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

    p = argparse.ArgumentParser(description="Convert bpftrace's 'nsecs since boot' timestamps to a UTC")
    p.add_argument("traces_dir", help="Directory where raw traces are")
    p.add_argument("output_dir", help="Directory where to write the time aligned traces")
    p.add_argument("ref_timestamp", type=int,
        help="Reference timestamp, for which the equivalent local time is known")
    p.add_argument("ref_localtime", 
        help="Reference local time, for which the equivalent timestamp is known. Format: 'YYYY-mm-ddTHH:MM:SS.fffffffff'")

    args = p.parse_args()

    if not os.path.isdir(args.traces_dir):
        print(f"Invalid trace directory")
        exit(-1) 

    pathlib.Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    if not os.path.isdir(args.output_dir):
        print(f"Invalid output directory")
        exit(-1) 

    main(args.traces_dir, args.output_dir, args.ref_timestamp, np.datetime64(args.ref_localtime))

