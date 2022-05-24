import os
import re
import pathlib
import numpy as np
import argparse

# Add any new trace we want to time align here
TRACES = ["openat", "close", "read", "write", "mmap", "create_del", "bio"]


def get_ref_ts(timealign_trace, gpu_trace):

    timealign_trace = open(timealign_trace, "r")
    
    # Expected trace line format: a nsecs since boot timestamp followed by a local time
    pat = re.compile(r'(\d+)\s+(\d{2}:\d{2}:\d{2})\n')

    min_ts_diff = float('inf')
    min_lt_0 = None
    min_lt_1 = None
    
    # Discard the first lines of the trace file until we get content
    line = timealign_trace.readline()
    while not pat.match(line):
        line = timealign_trace.readline()

    # Get the initial local time
    prev_lt = pat.match(line).group(2) # local time
    # Keep iterating on the file until we find the next seconds transition
    prev_ts = pat.match(line).group(1)

    for line in timealign_trace:
        if match := pat.match(line):
            ts = match.group(1) # time stamp (nsecs since boot)
            lt = match.group(2) # local time

            # If the current line's local time is not equal to the saved one
            # then we have a seconds transition. Subtract the current timestamp
            # from the previous one and save the smallest we find.
            if lt != prev_lt:
                diff = int(ts) - int(prev_ts)

                if diff < min_ts_diff:
                    min_ts_diff = diff

                    min_ts_0 = prev_ts
                    min_ts_1 = ts
                    min_lt_0 = prev_lt
                    min_lt_1 = lt
                    print(f"New min timestamp diff found btw {prev_lt} and {lt}: {min_ts_diff}")

                prev_lt = lt

            prev_ts = ts

    print(f"Min timestamp diff is {min_ts_diff} ns between {min_lt_0} and {min_lt_1}")

    ref_ts = int(min_ts_1) - (min_ts_diff // 2)
    ref_lt = min_lt_1

    print(f"We'll say ts {ref_ts} corresponds to {ref_lt}.000000000")

    # Try to get the date from the GPU trace
    gpu_trace = open(gpu_trace, "r")

    pat = re.compile(r'^\s+(\d{8})\s+(\d{2}:\d{2}:\d{2}).*')

    localdate = None
    for line in gpu_trace:
        if match := pat.match(line):
            localdate = match.group(1)
            print(f"Found the local date in gpu trace: {localdate}")
            break

    # Gpu trace localdate is in YYYYMMDD, break it into YYYY-MM-DD
    utc_str = f"{localdate[0:4]}-{localdate[4:6]}-{localdate[6:]}T{ref_lt}.000000000"
    ref_UTC = np.datetime64(utc_str)
    print(ref_UTC)

    return ref_ts, ref_UTC


def align_all_traces(traces_dir, output_dir, ref_ts, ref_t):

    # Add 5 hours to convert to UTC (we are in Montreal time)
    ref_t = ref_t + np.timedelta64(5, "h")

    for trace in TRACES:

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
    args = p.parse_args()

    if not os.path.isdir(args.traces_dir):
        print(f"Invalid trace directory")
        exit(-1) 

    time_align_trace = os.path.join(args.traces_dir, "trace_time_align.out")
    if not os.path.isfile(time_align_trace):
        print(f"ERROR: Could not find trace_time_align.out in {args.traces_dir}.")
        exit(-1) 

    gpu_trace = os.path.join(args.traces_dir, "gpu.out")
    print(gpu_trace)
    if not os.path.isfile(gpu_trace):
        print(f"ERROR: Could not find gpu.out in {args.traces_dir}")
        exit(-1) 

    ref_ts, ref_UTC = get_ref_ts(time_align_trace, gpu_trace)
    align_all_traces(args.traces_dir, args.output_dir, ref_ts, ref_UTC)

