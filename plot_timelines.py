import matplotlib
from matplotlib import dates as mdates, pyplot as plt, patches as mpatches, colors
import numpy as np
import pandas as pd
from collections import defaultdict
import os.path

DATA_DIR = "data/timeline_data/4gpu_baseline"

def plot_thread(pid):

    fig, ax = plt.subplots(figsize=(20, 6))

    df = pd.read_csv(
        f"data/st_end_data/st_end_data_{pid.split('_')[0]}",
        names=["start_date", "end_date", "event"],
    )
    df = df[["start_date", "end_date", "event"]]
    df.start_date = pd.to_datetime(df.start_date).astype(np.datetime64)
    df.end_date = pd.to_datetime(df.end_date).astype(np.datetime64)

    if pid == "1313336_p1":
        df = df[df["end_date"] < np.datetime64("2022-02-05T21:00:00")]
    elif pid == "1313336_p2":
        df = df[df["end_date"] > np.datetime64("2022-02-05T21:00:00")]

    print(df.shape)

    bar_height = 1
    colors_dict = dict(
        OPENAT="purple",
        VFSOPEN="slateblue",
        VFSR="dodgerblue",
        VFSW="red",
        BIOR="darkorange",
        BIOW="red",
    )

    ymins = [0, 1, 2]
    categories = ["BIO", "VFS", "OPEN"]
    masks = {
        "BIO": (df["event"] == "BIOR") | (df["event"] == "BIOW"),
        "OPEN": (df["event"] == "OPENAT") | (df["event"] == "VFSOPEN"),
        "R/W": (df["event"] == "READ") | (df["event"] == "WRITE"),
    }

    # Plot the events
    for i, category in enumerate(categories):
        mask = masks[category]
        start_dates = mdates.date2num(df.loc[mask].start_date)
        print(start_dates)
        end_dates = mdates.date2num(df.loc[mask].end_date)
        durations = end_dates - start_dates
        xranges = list(zip(start_dates, durations))
        ymin = ymins[i] - 0.5
        yrange = (ymin, bar_height)
        colors = [colors_dict[event] for event in df.loc[mask].event]
        ax.broken_barh(xranges, yrange, facecolors=colors, alpha=1)
        # you can set alpha to 0.6 to check if there are some overlaps

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # Specific formatting for each pid

    if pid == "1313298":
        # Format the x-ticks
        ax.xaxis.set_major_locator(mdates.SecondLocator())
        ax.xaxis.set_minor_locator(mdates.MicrosecondLocator(interval=100_000))

        ax.xaxis.set_major_formatter(
            mdates.DateFormatter(
                "%H:%M:%S",
            )
        )
        # Set the limits
        ax.set_xlim(
            (df.start_date.min() - np.timedelta64(500, "ms")).round(freq="S"),
            (df.start_date.max() + np.timedelta64(100, "ms")),
        )
        ax.grid(True, axis="x", which="minor", linestyle="--", linewidth=0.2)
        ax.grid(True, axis="x", which="major", linestyle="--", linewidth=0.5)
        ax.tick_params(
            axis="x", which="both", direction="in", grid_color="grey", grid_alpha=0.2, rotation=30
        )
    elif pid == "1313302":

        ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=100))
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter(
                ".%f",
            )
        )
        ax.text(-0.041, -0.278, "20:27:40", transform=ax.transAxes, fontsize=12, rotation=45)
        plt.gcf().subplots_adjust(bottom=0.25)

        print(df.start_date.min())
        print(df.start_date.max())
        # Set the limits
        ax.set_xlim(
            df.start_date.min() - np.timedelta64(10, "us"),
            df.start_date.max() + np.timedelta64(10, "us"),
        )

        ax.grid(True, axis="x", which="major", linestyle="--", linewidth=0.5)
        ax.tick_params(
            axis="x",
            which="major",
            labelsize=10,
            direction="in",
            grid_color="grey",
            grid_alpha=0.2,
            rotation=45,
        )
    elif pid == "1313336_p1" or pid == "1313336_p2":
        ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=5))
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter(
                "%H:%M:%S",
            )
        )
        ax.xaxis.set_minor_locator(mdates.AutoDateLocator(maxticks=100))
        ax.xaxis.set_minor_formatter(
            mdates.DateFormatter(
                ".%f",
            )
        )
        plt.gcf().subplots_adjust(bottom=0.25)

        print(df.start_date.min())
        print(df.start_date.max())
        # Set the limits
        ax.set_xlim(
            df.start_date.min() - np.timedelta64(10, "us"),
            df.start_date.max() + np.timedelta64(10, "us"),
        )

        ax.grid(True, axis="x", which="minor", linestyle="--", linewidth=0.25)
        ax.tick_params(
            axis="x",
            which="major",
            labelsize=12,
            direction="in",
            grid_color="grey",
            grid_alpha=0.2,
            rotation=45,
        )
        ax.tick_params(
            axis="x",
            which="minor",
            labelsize=8,
            direction="in",
            grid_color="grey",
            grid_alpha=0.2,
            rotation=45,
        )
    else:
        # Default formatting
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter(
                "%b%d",
            )
        )
        ax.xaxis.set_minor_locator(mdates.AutoDateLocator(maxticks=100))
        ax.xaxis.set_minor_formatter(
            mdates.DateFormatter(
                "%H:%M:%S",
            )
        )

        print(df.start_date.min())
        print(df.start_date.max())
        # Set the limits
        ax.set_xlim(
            df.start_date.min() - np.timedelta64(5, "m"),
            df.start_date.max() + np.timedelta64(5, "m"),
        )

        ax.grid(True, axis="x", which="minor", linestyle="--", linewidth=0.45)
        ax.tick_params(
            axis="x", which="both", direction="in", grid_color="grey", grid_alpha=0.2, rotation=30
        )
        ax.tick_params(axis="x", which="major", labelsize=12)
        ax.tick_params(axis="x", which="minor", labelsize=8)

    # Format the y-ticks
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories)

    # Add the legend
    patches = [mpatches.Patch(color=color, label=key) for (key, color) in colors_dict.items()]
    ax.legend(handles=patches, bbox_to_anchor=(1, 0.5), loc="center left")

    ax.set_title(pid)

    plt.savefig(f"./plots/timelines/{pid}.png", format="png", dpi=500)


def plot_threads_w_timeline():

    pids = [
        # "1313298", These 3 are too short-lived to show up
        # "1313302",
        # "1313336",
        "1313402",
        "1313403",
        "1313404",
        "1313405",
        "1313406",
        "1313407",
        "1313408",
        "1313409",
    ]

    bar_height = 1
    ymins = [0, 1, 2]
    categories = ["BIO", "VFS", "OPEN"]
    colors_dict = dict(
        OPENAT="purple",
        VFSOPEN="slateblue",
        VFSR="dodgerblue",
        VFSW="red",
        BIOR="darkorange",
        BIOW="red",
    )

    fig, axs = plt.subplots(
        nrows=len(pids) + 1,
        ncols=1,
        figsize=(30, len(pids) * 3),
        gridspec_kw={"height_ratios": [3] * len(pids) + [1]},  # 1 for timeline
        sharex=True,
    )

    for i, pid in enumerate(pids):
        #
        # PLOT thread events
        #
        print(f"Processing pid {pid}")

        df = pd.read_csv(
            f"data/st_end_data/st_end_data_{pid}", names=["start_date", "end_date", "event"]
        )
        df = df[["start_date", "end_date", "event"]]
        df.start_date = pd.to_datetime(df.start_date).astype(np.datetime64)
        df.end_date = pd.to_datetime(df.end_date).astype(np.datetime64)

        # Can't define this earlier
        masks = {
            "BIO": (df["event"] == "BIOR") | (df["event"] == "BIOW"),
            "OPEN": (df["event"] == "OPENAT") | (df["event"] == "VFSOPEN"),
            "R/W": (df["event"] == "READ") | (df["event"] == "WRITE"),
        }

        ax = axs[i]
        ax.set_title(f"{pid}")

        # Plot the events
        for j, category in enumerate(categories):
            mask = masks[category]
            start_dates = mdates.date2num(df.loc[mask].start_date)
            end_dates = mdates.date2num(df.loc[mask].end_date)
            # print(start_dates)
            # print(end_dates)
            # Could increase bar width by rounding up durations to nearest ms or such
            durations = end_dates - start_dates
            print(durations)
            xranges = list(zip(start_dates, durations))
            ymin = ymins[j] - 0.5
            yrange = (ymin, bar_height)
            colors = [colors_dict[event] for event in df.loc[mask].event]
            ax.broken_barh(xranges, yrange, facecolors=colors, alpha=1)
            # you can set alpha to 0.6 to check if there are some overlaps

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

        ax.grid(True, axis="x", linestyle="--", linewidth=0.45, alpha=0.2, color="grey")
        ax.tick_params(which="both", direction="in")

        # Format the x-ticks
        ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=100))
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter(
                "%H:%M:%S",
            )
        )

        # Format the y-ticks
        ax.set_yticks(range(len(categories)))
        ax.set_yticklabels(categories)

        # Add the legend
        if i == 4:
            patches = [
                mpatches.Patch(color=color, label=key) for (key, color) in colors_dict.items()
            ]
            ax.legend(handles=patches, bbox_to_anchor=(1, 0.5), loc="center left")

    #
    # Plot the timeline
    #
    print(f"Processing timeline")

    df = pd.read_csv("data/mllog_data/timeline.csv", names=["start_date", "end_date", "event"])

    df = df[["start_date", "end_date", "event"]]
    df.start_date = pd.to_datetime(df.start_date).astype(np.datetime64)
    df.end_date = pd.to_datetime(df.end_date).astype(np.datetime64)

    categories = ["Training"]

    ymins = [0]
    colors_dict = dict(INIT="blue", EPOCH="gold", EVAL="darkorchid")

    # Select the last axes
    ax = axs[-1]

    # Plot the events
    for i, category in enumerate(categories):
        start_dates = mdates.date2num(df.start_date)
        end_dates = mdates.date2num(df.end_date)
        durations = end_dates - start_dates
        xranges = list(zip(start_dates, durations))
        ymin = ymins[i] - 0.5
        yrange = (ymin, bar_height)
        colors = [colors_dict[event] for event in df.event]
        ax.broken_barh(xranges, yrange, facecolors=colors, alpha=0.8)
        # you can set alpha to 0.6 to check if there are some overlaps

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # Add the legend
    patches = [mpatches.Patch(color=color, label=key) for (key, color) in colors_dict.items()]
    ax.legend(handles=patches, bbox_to_anchor=(1, 0.5), loc="center left")

    # Set the x axis limits
    ax.set_xlim(
        df.start_date.min() - np.timedelta64(10, "m"),
        df.start_date.max() + np.timedelta64(10, "m"),
    )

    # Format the x-ticks
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=100))
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter(
            "%b%d %H:%M",
        )
    )

    # Format the y-ticks
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories)

    ax.grid(True, axis="x", which="major", linestyle="--", linewidth=0.45, alpha=0.2, color="grey")
    ax.tick_params(
        axis="x",
        which="major",
        direction="out",
        labelsize=12,
        rotation=30,
    )

    print("Saving figure")
    fig.suptitle("MLCommons Image Segmentation")

    plt.savefig("./plots/timelines/all_threads_2.png", format="png", dpi=600)


def generate_all_indiv_thread_plots():
    pids = [
        "1313298",
        "1313302",
        "1313336_p1",
        "1313336_p2",
        "1313402",
        "1313403",
        "1313404",
        "1313405",
        "1313406",
        "1313407",
        "1313408",
        "1313409",
    ]
    for pid in pids:
        plot_thread(pid)


def plot_timeline_cpu_gpu(start=None, end=None, outname=None):

    bar_height = 1
    ymins = [0, 1, 2]
    categories = ["BIO", "R/W", "OPEN"]
    colors_dict = dict(
        OPENAT="purple",
        READ="dodgerblue",
        WRITE="red",
        BIOR="darkorange",
        BIOW="red",
    )

    fig, axs = plt.subplots(
        nrows=3,
        ncols=1,
        figsize=(30, 10),
        gridspec_kw={"height_ratios": [3, 3, 1]},  # 1 for timeline
        sharex=True,
    )

    #
    # Plot CPU
    #
    df = pd.read_csv(
        f"data/cpu_data/cpu_all.csv",
        sep=",",
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    if start is not None:
        df = df[df["timestamp"] > np.datetime64(start)]
    if end is not None:
        df = df[df["timestamp"] < np.datetime64(end)]

    print(f"CPU data read: {df.shape}")

    ax = axs[0]

    ax.set_title("CPU Usage")

    ax.set_ylabel("percent utilisation(%)")

    # There are more fields available but weren't very interesting
    variables = [
        "%usr",
        "%sys",
        "%iowait",
        "%idle",
    ]

    n_features = len(variables)

    cm = plt.get_cmap("gist_rainbow")  # Colormap

    for i, var in enumerate(variables):
        line = ax.plot(df["timestamp"], df[var], label=var, linewidth=1)
        line[0].set_color(cm(1 * i / n_features))

    ax.grid(True, which="both", linestyle="--", color="grey", alpha=0.2)
    ax.tick_params(which="both", direction="in")

    ax.set_ylim(ymin=0)
    ax.legend(bbox_to_anchor=(1, 0.5), loc="center left")

    ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=100))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

    #
    # Plot GPU
    #
    df = pd.read_csv(f"./data/gpu_data/gpu_avg.csv", sep=",")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    if start is not None:
        df = df[df["timestamp"] > np.datetime64(start)]
    if end is not None:
        df = df[df["timestamp"] < np.datetime64(end)]

    ax1 = axs[1]

    ax1.set_title("GPU Usage")

    ax1.set_ylabel("percent utilisation(%)")

    ax1.plot(
        df["timestamp"],
        df["sm"],
        label="GPU MultiProcessor Use (%)",
        color="tab:red",
        linewidth=1,
        markersize=5,
    )
    ax1.plot(
        df["timestamp"],
        df["mem"],
        label="GPU Memory Use (%)",
        color="tab:orange",
        linewidth=1,
        markersize=5,
    )

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    ax2.set_ylabel("Size (MB)")
    ax2.plot(
        df["timestamp"],
        df["fb"],
        label="Framebuffer memory use (MB)",
        color="tab:blue",
        linewidth=1.5,
        markersize=5,
    )

    ax1.grid(True, which="both", linestyle="--")
    ax1.tick_params(which="both", direction="in", grid_color="grey", grid_alpha=0.2)

    ax1.set_ylim(ymin=0)
    ax2.set_ylim(ymin=0)

    ax1.legend(loc="center left")
    ax2.legend(loc="center right")

    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

    # https://matplotlib.org/stable/api/ticker_api.html#matplotlib.ticker.Locator
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=100))
    ax2.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=100))

    #
    # Plot the timeline
    #
    print(f"Processing timeline")

    df = pd.read_csv("data/mllog_data/timeline.csv", names=["start_date", "end_date", "event"])

    df = df[["start_date", "end_date", "event"]]
    df.start_date = pd.to_datetime(df.start_date).astype(np.datetime64)
    df.end_date = pd.to_datetime(df.end_date).astype(np.datetime64)

    if start is not None:
        df = df[df["end_date"] > np.datetime64(start)]
    if end is not None:
        df = df[df["end_date"] < np.datetime64(end)]

    categories = ["Training"]

    ymins = [0]
    colors_dict = dict(INIT="blue", EPOCH="gold", EVAL="darkorchid")

    # Select the last axes
    ax = axs[-1]

    # Plot the events
    for i, category in enumerate(categories):
        start_dates = mdates.date2num(df.start_date)
        end_dates = mdates.date2num(df.end_date)
        durations = end_dates - start_dates
        xranges = list(zip(start_dates, durations))
        ymin = ymins[i] - 0.5
        yrange = (ymin, bar_height)
        colors = [colors_dict[event] for event in df.event]
        ax.broken_barh(xranges, yrange, facecolors=colors, alpha=0.8)
        # you can set alpha to 0.6 to check if there are some overlaps

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # Add the legend
    patches = [mpatches.Patch(color=color, label=key) for (key, color) in colors_dict.items()]
    ax.legend(handles=patches, bbox_to_anchor=(1, 0.5), loc="center left")

    # Format the x-ticks
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=100))
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter(
            "%b %d %H:%M",
        )
    )

    # Set the x axis limits
    ax.set_xlim(
        df.start_date.min() - np.timedelta64(30, "s"),
        df.start_date.max() + np.timedelta64(30, "s"),
    )

    # Format the y-ticks
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories)

    ax.grid(True, axis="x", linestyle="--", linewidth=0.45, alpha=0.2, color="grey")
    ax.tick_params(axis="x", which="both", direction="out", rotation=30)

    print("Saving figure")

    fig.suptitle("MLCommons Image Segmentation")

    if outname is not None:
        filename = outname
    else:
        filename = "cpu_gpu_timeline"

    plt.savefig(f"./plots/{filename}.png", format="png", dpi=600)


def plot_pids_timeline_cpu_gpu(pids, pid_names, title, start=None, end=None, margin=np.timedelta64(60, "s"), filename=None):

    bar_height = 1
    ymins = [0, 1, 2]
    categories = ["BIO", "R/W", "OPEN"]
    colors_dict = dict(
        OPENAT="purple",
        READ="dodgerblue",
        WRITE="red",
        BIOR="blue",
        BIOW="red",
    )

    fig, axs = plt.subplots(
        nrows=len(pids) + 3,
        ncols=1,
        figsize=(30, len(pids) * 3),
        gridspec_kw={"height_ratios": [3] * (len(pids) + 2) + [1]},  # 1 for timeline
        sharex=True,
    )

    #
    # Plot CPU
    #
    df = pd.read_csv(
        os.path.join(DATA_DIR, "cpu_data/cpu_all.csv"),
        sep=",",
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    if start is not None:
        df = df[df["timestamp"] > np.datetime64(start)]
    if end is not None:
        df = df[df["timestamp"] < np.datetime64(end)]

    ax = axs[0]
    ax.set_title("CPU Usage")
    ax.set_ylabel("percent utilisation(%)")

    # There are more fields available but weren't very interesting
    variables = [
        "%usr",
        "%sys",
        "%iowait",
        "%idle",
    ]

    n_features = len(variables)

    cm = plt.get_cmap("gist_rainbow")  # Colormap

    for i, var in enumerate(variables):
        line = ax.plot(df["timestamp"], df[var], label=var, linewidth=1)
        line[0].set_color(cm(1 * i / n_features))

    ax.grid(True, which="both", linestyle="--", color="grey", alpha=0.2)
    ax.tick_params(which="both", direction="in")

    ax.set_ylim(ymin=0)
    ax.legend(bbox_to_anchor=(1, 0.5), loc="center left")

    # ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=100))
    # ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

    #
    # Plot GPU
    #
    df = pd.read_csv(os.path.join(DATA_DIR, "gpu_data/gpu_avg.csv"), sep=",")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    if start is not None:
        df = df[df["timestamp"] > np.datetime64(start)]
    if end is not None:
        df = df[df["timestamp"] < np.datetime64(end)]

    ax1 = axs[1]
    ax1.set_title("GPU Usage")
    ax1.set_ylabel("percent utilisation(%)")

    ax1.plot(
        df["timestamp"],
        df["sm"],
        label="GPU MultiProcessor Use (%)",
        color="tab:red",
        linewidth=1,
        markersize=5,
    )
    ax1.plot(
        df["timestamp"],
        df["mem"],
        label="GPU Memory Use (%)",
        color="tab:orange",
        linewidth=1,
        markersize=5,
    )

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    ax2.set_ylabel("Size (MB)")
    ax2.plot(
        df["timestamp"],
        df["fb"],
        label="Framebuffer memory use (MB)",
        color="tab:blue",
        linewidth=1.5,
        markersize=5,
    )

    ax1.grid(True, which="both", linestyle="--")
    ax1.tick_params(which="both", direction="in", grid_color="grey", grid_alpha=0.2)

    ax1.set_ylim(ymin=0)
    ax2.set_ylim(ymin=0)

    ax1.legend(loc="center left")
    ax2.legend(loc="center right")

    # ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    # ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

    # ax1.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=100))
    # ax2.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=100))

    #
    # Plot PIDs
    #
    for i, pid in enumerate(pids):
        print(f"Processing pid {pid}")

        df = pd.read_csv(
            os.path.join(DATA_DIR, f"st_end_data/st_end_data_{pid}"), names=["start_date", "end_date", "event"]
        )
        df = df[["start_date", "end_date", "event"]]
        df.start_date = pd.to_datetime(df.start_date).astype(np.datetime64)
        df.end_date = pd.to_datetime(df.end_date).astype(np.datetime64)

        if start is not None:
            df = df[df["end_date"] > np.datetime64(start)]
        if end is not None:
            df = df[df["end_date"] < np.datetime64(end)]

        # Can't define this earlier
        masks = {
            "BIO": (df["event"] == "BIOR") | (df["event"] == "BIOW"),
            "OPEN": (df["event"] == "OPENAT") ,
            "R/W": (df["event"] == "READ") | (df["event"] == "WRITE"),
        }

        ax = axs[i + 2]
        if pid in pid_names:
            title = pid_names[pid] 
        else:
            title = pid

        ax.set_title(f"{title}")

        # Plot the events
        for j, category in enumerate(categories):
            mask = masks[category]
            start_dates = mdates.date2num(df.loc[mask].start_date)
            end_dates = mdates.date2num(df.loc[mask].end_date)
            durations = end_dates - start_dates
            xranges = list(zip(start_dates, durations))
            ymin = ymins[j] - 0.5
            yrange = (ymin, bar_height)
            colors = [colors_dict[event] for event in df.loc[mask].event]
            ax.broken_barh(xranges, yrange, facecolors=colors, alpha=1)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

        ax.grid(True, axis="both", linestyle="--", linewidth=0.45, alpha=0.2, color="grey")
        ax.tick_params(which="both", direction="in")

        # Format the y-ticks
        ax.set_yticks(range(len(categories)))
        ax.set_yticklabels(categories)

        # Add the legend
        if i == 3:
            patches = [
                mpatches.Patch(color=color, label=key) for (key, color) in colors_dict.items()
            ]
            ax.legend(handles=patches, bbox_to_anchor=(1, 0.5), loc="center left")

    #
    # Plot the timeline
    #
    print(f"Processing timeline")

    df = pd.read_csv(os.path.join(DATA_DIR, "mllog_data/timeline.csv"), names=["start_date", "end_date", "event"])

    df = df[["start_date", "end_date", "event"]]
    df.start_date = pd.to_datetime(df.start_date).astype(np.datetime64)
    df.end_date = pd.to_datetime(df.end_date).astype(np.datetime64)

    if start is not None:
        df = df[df["end_date"] > np.datetime64(start)]
    if end is not None:
        df = df[df["end_date"] < np.datetime64(end)]

    categories = ["Training"]

    ymins = [0]
    colors_dict = dict(INIT="blue", EPOCH="gold", EVAL="darkorchid")

    # Select the last axes
    ax = axs[-1]

    # Plot the events
    for i, category in enumerate(categories):
        start_dates = mdates.date2num(df.start_date)
        end_dates = mdates.date2num(df.end_date)
        durations = end_dates - start_dates
        xranges = list(zip(start_dates, durations))
        ymin = ymins[i] - 0.5
        yrange = (ymin, bar_height)
        colors = [colors_dict[event] for event in df.event]
        ax.broken_barh(xranges, yrange, facecolors=colors, alpha=0.8)
        # you can set alpha to 0.6 to check if there are some overlaps

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # Add the legend
    patches = [mpatches.Patch(color=color, label=key) for (key, color) in colors_dict.items()]
    ax.legend(handles=patches, bbox_to_anchor=(1, 0.5), loc="center left")

    # TODO: Calculate the sort of timescale we're plotting and choose appropriate limits
    # Format the x-ticks
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=100))
    ax.xaxis.set_major_formatter(mdates.DateFormatter(
            "%H:%M",
            # "%H:%M:%S.%f",
    ))

    # TODO: Calculate the sort of timescale we're plotting and choose appropriate limits
    # Set the x axis limits
    if margin is None:
        margin = np.timedelta64(60, "s")

    ax.set_xlim(
        df.start_date.min() - margin,
        df.end_date.max() + margin,
    )

    # Format the y-ticks
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories)

    ax.grid(True, axis="x", linestyle="--", linewidth=0.45, alpha=0.2, color="grey")
    ax.tick_params(axis="x", which="both", direction="out", rotation=30)

    print("Saving figure")

    fig.suptitle(title)

    if filename is not None:
        filename = filename
    else:
        filename = "timelines/cpu_gpu_timeline"

    plt.savefig(f"./plots/{filename}.png", format="png", dpi=600)


if __name__ == "__main__":

    DATA_DIR = "data/timeline_data/4gpu_baseline"

    pids = [
        # "32260",       # Possibly just loading the mllog library
        # "32261",
        "32263",        # Main process
        # "32264",
        "32296",        # Multiprocessing resource tracker
        "32297",        # Workers 
        "32298",
        "32299",
        "32300",
    ]

    pid_names = {
        "32263": "master process",
        "32296": "resource tracker", 
        "32297": "worker 1",        
        "32298": "worker 2",
        "32299": "worker 3",
        "32300": "worker 4",
    }

    # plot_pids_timeline_cpu_gpu(
    #     pids, pid_names,
    #     title="MLCommons Image Segmentation - 4 GPUs Baseline",
    #     filename="timelines/4gpu_baseline",
    # )

    # plot_pids_timeline_cpu_gpu(
    #     pids, pid_names,
    #     title="MLCommons Image Segmentation - 4 GPUs Baseline - First 5 Minutes",
    #     start="2022-04-29T18:15:30",
    #     end="2022-04-29T18:20:30",
    #     margin=np.timedelta64(15, "s"),
    #     filename="timelines/4gpu_baseline_first5min",
    # )

    # plot_pids_timeline_cpu_gpu(
    #     pids, pid_names,
    #     title="MLCommons Image Segmentation - 4 GPUs Baseline - First Evaluation Period",
    #     start="2022-04-29T18:30:30",
    #     end="2022-04-29T18:33:30",
    #     margin=np.timedelta64(5, "s"),
    #     filename="timelines/4gpu_baseline_firsteval",
    # )
