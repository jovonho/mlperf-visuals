import os.path
import numpy as np
import pandas as pd

def get_cpu_stats(start=None, end=None):

    df = pd.read_csv(os.path.join(DATA_DIR, "gpu_data/gpu_avg.csv"), sep=",")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    if start is not None:
        df = df[df["timestamp"] > np.datetime64(start)]
    if end is not None:
        df = df[df["timestamp"] < np.datetime64(end)]

    stats=pd.DataFrame()
    stats["mean"]=df.mean()
    stats["Std.Dev"]=df.std()
    stats["Var"]=df.var()

    print(stats.T)


if __name__ == "__main__":

    DATA_DIR = "ta_4gpus_100gb"
    # First epoch to first eval for 1xRAM
    get_cpu_stats(start="2022-05-11T23:50:47", end="2022-05-11T23:52:57")