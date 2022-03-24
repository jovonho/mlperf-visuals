from matplotlib import dates, pyplot as plt
import numpy as np
import pandas as pd


def plot_gpu(filename="gpu_avg"):

    gpu = pd.read_csv(f"./data/gpu_data/{filename}.csv", sep=",")
    gpu["timestamp"] = pd.to_datetime(gpu["timestamp"])

    print(f"Data read: {gpu.shape}\n{gpu.dtypes}")

    fig, ax1 = plt.subplots()

    fig.autofmt_xdate()
    ax1.set_title("MLPerf Image Segmentation: GPU Usage")
    fig.set_size_inches(18.5, 10.5)

    ax1.set_xlabel("timestamp")
    ax1.set_ylabel("percent utilisation(%)")

    ax1.plot(
        gpu["timestamp"],
        gpu["sm"],
        label="GPU MultiProcessor Use (%)",
        color="tab:red",
        linewidth=0.5,
        markersize=5,
    )
    ax1.plot(
        gpu["timestamp"],
        gpu["mem"],
        label="GPU Memory Use (%)",
        color="tab:orange",
        linewidth=0.5,
        markersize=5,
    )

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    ax2.set_ylabel("Size (MB)")
    ax2.plot(
        gpu["timestamp"],
        gpu["fb"],
        label="Framebuffer memory use (MB)",
        color="tab:blue",
        linewidth=1.5,
        markersize=5,
    )

    ax1.grid(True, which="both", linestyle="--")
    ax1.tick_params(which="both", direction="in", grid_color="grey", grid_alpha=0.2)

    ax1.set_ylim(ymin=0)
    ax2.set_ylim(ymin=0)

    ax1.legend(loc=(0, 1.02))
    ax2.legend(loc=(0.8, 1.02))

    xfmt = dates.DateFormatter("%H:%M:%S")

    ax1.xaxis.set_major_formatter(xfmt)
    ax2.xaxis.set_major_formatter(xfmt)

    # https://matplotlib.org/stable/api/ticker_api.html#matplotlib.ticker.Locator
    ax1.xaxis.set_major_locator(dates.AutoDateLocator(maxticks=100))
    ax2.xaxis.set_major_locator(dates.AutoDateLocator(maxticks=100))

    print("Axes setup. Saving Figure.")
    plt.savefig(f"./plots/gpu_plots/{filename}.png", format="png", dpi=300)


def plot_cpu(filename="cpu_all"):

    df = pd.read_csv(
        f"data/cpu_data/{filename}.csv",
        sep=",",
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    print(f"Data read: {df.shape}")
    print(df.dtypes)

    fig, ax1 = plt.subplots()

    fig.autofmt_xdate()

    ax1.set_title("MLPerf Image Segmentation: CPU Usage")
    fig.set_size_inches(18.5, 10.5)

    ax1.set_xlabel("timestamp")
    ax1.set_ylabel("percent utilisation(%)")

    variables = [
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

    n_features = len(variables)

    cm = plt.get_cmap("gist_rainbow")  # Colormap

    for i, var in enumerate(variables):
        line = ax1.plot(df["timestamp"], df[var], label=var, linewidth=0.5)
        line[0].set_color(cm(1 * i / n_features))

    ax1.grid(True, which="both", linestyle="--")
    ax1.tick_params(which="both", direction="in", grid_color="grey", grid_alpha=0.2)

    ax1.set_ylim(ymin=0)

    ax1.legend()

    xfmt = dates.DateFormatter("%H:%M:%S")

    ax1.xaxis.set_major_formatter(xfmt)

    # https://matplotlib.org/stable/api/ticker_api.html#matplotlib.ticker.Locator
    ax1.xaxis.set_major_locator(dates.AutoDateLocator(maxticks=100))

    print("Axes setup. Saving Figure.")
    plt.savefig(f"./plots/cpu_plots/{filename}.png", format="png", dpi=300)


if __name__ == "__main__":

    names = ["gpu_avg", "gpu_avg_first5min", "gpu_avg_30min_phase1", "gpu_avg_30min_phase2"]
    for name in names:
        plot_gpu(name)

    names = ["cpu_all", "cpu_all_first5min", "cpu_all_30min_phase1", "cpu_all_30min_phase2"]

    for name in names:
        plot_cpu(name)
