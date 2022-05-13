import os
import argparse
import numpy as np

#TODO changig dates


def main(cpu_trace):
    """
    Convert raw cpu usage data to a csv file
    """
    # Change this
    current_date = "2022-05-11"

    data_dir = os.path.dirname(cpu_trace)

    infile = open(cpu_trace, "r")
    outcsv = open(os.path.join(data_dir, "cpu_all.csv"), "w")

    # Print headers
    headers = [
        "timestamp",
        "%usr",
        "%nice",
        "%sys",
        "%iowait",
        "%irq",
        "%soft",
        "%steal",
        "%guest",
        "%gnice",
        "%idle",
    ]
    outcsv.write(",".join(headers) + "\n")

    date_changed = False

    for line in infile:
        # Remove duplicate spaces, and split
        cols = " ".join(line.replace("all", "").split()).split(" ")

        # Don't process the last line
        if cols[0] == "Average:":
            break

        if not date_changed and cols[0] == "00:00:00":
            current_date = "2022-05-12"
            date_changed = True

        # Make UTC timestamp from time and current date
        cols[0] = str(np.datetime64(current_date + "T" + cols[0]) + np.timedelta64(5, "h"))
        outcsv.write(",".join(cols) + "\n")

    infile.close()
    outcsv.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generates a CSV from an mpstat trace of average cpu usage")
    p.add_argument("cpu_trace", help="The mpstat trace, containing only the lines for 'all'")
    # p.add_argument("current_date", help="The date of the trace")
    args = p.parse_args()

    if not os.path.isfile(args.cpu_trace):
        print(f"Invalid trace file given")
        exit(-1) 

    main(args.cpu_trace)
