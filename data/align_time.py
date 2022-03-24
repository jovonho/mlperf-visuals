import numpy as np


def main():
    # Obtained from previous analysis
    ref_ts = 1380360127458684
    # Add 5h to convert from EST to UTC
    ref_t = np.datetime64("2022-02-05T15:28:13.000000000") + np.timedelta64(5, "h")

    traces = ["bio", "vfs_rw", "open"]
    # traces = ["open"]

    for trace in traces:
        infile = open(trace + ".out", "r")
        outfile = open(trace + "_time_aligned.out", "w")

        # Discard the first 2 lines of traces
        infile.readline()
        infile.readline()

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
            outfile.write(np.datetime_as_string(t) + " " + " ".join(cols[2::]) + "\n")


if __name__ == "__main__":
    main()
