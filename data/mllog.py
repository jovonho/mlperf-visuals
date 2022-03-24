import json
import os
import numpy as np


def process_timeline():
    """
    Convert the UNIX timestamps of the mllog to UTC timestamp
    """
    cwd = os.path.basename(os.getcwd())
    if cwd == "data":
        path = "mllog_data"
    else:
        path = "data/mllog_data"

    infile = open(f"{path}/timeline.log", "r")
    outfile = open(f"{path}/timeline.csv", "w")

    all_logs = json.load(infile)

    start_events = {}

    for i, log in enumerate(all_logs):

        ux_time = np.datetime64(log["time_ms"], "ms")

        key_parts = log["key"].split("_")

        key = key_parts[0].upper()
        key_type = key_parts[1]

        if key_type == "stop":
            if key not in start_events:
                print(f"No starting event for {log['key']} at ts {log['time_ms']}\n")
                continue
            else:
                outfile.write(f"{start_events[key]},{ux_time},{key}\n")
                del start_events[key]
        else:
            start_events[key] = ux_time


def process_vals():

    cwd = os.path.basename(os.getcwd())
    if cwd == "data":
        path = "mllog_data"
    else:
        path = "data/mllog_data"

    infile = open(f"{path}/evals.log", "r")
    outfile = open(f"{path}/evals.csv", "w")

    logs = json.load(infile)

    for log in logs:

        ux_time = np.datetime64(log["time_ms"], "ms")
        score = log["value"]

        outfile.write(f"{ux_time},{score}\n")


if __name__ == "__main__":
    process_vals()
