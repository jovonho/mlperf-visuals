import pandas as pd
import numpy as np


def main():
    """
    Convert raw cpu usage data to a csv file
    """
    # Change this
    current_date = "2022-02-05"

    infile = open("data/cpu_data/cpu.all", "r")
    outcsv = open("data/cpu_data/cpu_all.csv", "w")

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
            current_date = "2022-02-06"
            date_changed = True

        # Make UTC timestamp from time and current date
        cols[0] = str(np.datetime64(current_date + "T" + cols[0]) + np.timedelta64(5, "h"))
        outcsv.write(",".join(cols) + "\n")

    infile.close()
    outcsv.close()


if __name__ == "__main__":
    main()
