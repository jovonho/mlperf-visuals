import matplotlib
from matplotlib import dates as mdates, pyplot as plt, patches as mpatches, colors
import numpy as np
import pandas as pd
from collections import defaultdict


def plot_histograms_pids():

    pids = [
        "1313298",
        "1313302",
        "1313336",
        "1313402",
        "1313403",
        "1313404",
        "1313405",
        "1313406",
        "1313407",
        "1313408",
        "1313409",
    ]

    fig, axs_grid = plt.subplots(
        nrows=len(pids) + 1, ncols=7, figsize=(30, len(pids) * 3), sharex="col"
    )

    hists = [
        "bio_lat",
        "bio_size",
        "open_lat",
        "vfsopen_lat",
        "vfsrw_lat",
        "vfsrw_sizereq",
        "vfsrw_sizeret",
    ]

    columns_by_type = {
        "bio": ["rw", "lat", "size"],
        "open": ["lat"],
        "vfsopen": ["lat"],
        "vfsrw": ["rw", "lat", "sizereq", "sizeret"],
    }

    #
    # Plot PIDs
    #
    for i, pid in enumerate(pids):
        print(f"Processing pid {pid}")
        axs_line = axs_grid[i]

        # for type in ["bio", "open", "vfsopen", "vfsrw"]:

        #     datafile = f"data/{type}_data_hist/hist_{type}_{pid}"
        #     df = pd.read_csv(datafile, names=columns_by_type[type])

        #     ax = axs_line[0]

        for j, hist in enumerate(hists):
            print(f"\tPlotting {hist}")
            ax = axs_line[j]

            # Print titles for the first line
            if i == 0:
                ax.set_title(hist)

            if j == 0:
                ax.text(-0.5, 0.5, str(pid), transform=ax.transAxes, fontsize=12)

            # Plot legend
            if i == 3 and j == 6:
                colors_dict = {"R": "orange", "W": "blue", "NA": "green"}
                patches = [
                    mpatches.Patch(color=color, label=key) for (key, color) in colors_dict.items()
                ]
                ax.legend(handles=patches, bbox_to_anchor=(1, 0.5), loc="center left")

            type = hist.split("_")[0]
            hist_type = hist.split("_")[1]
            datafile = f"data/{type}_data_hist/hist_{type}_{pid}"
            cols = columns_by_type[type]
            df = pd.read_csv(datafile, names=cols)

            if "rw" in cols:
                # Plot double histos for R and W separately
                ax.hist(df[df["rw"] == "R"][hist_type], bins=25, color="orange", alpha=0.75)
                ax.hist(df[df["rw"] == "W"][hist_type], bins=25, color="blue", alpha=0.75)
            else:
                ax.hist(df[hist_type], bins=50, color="green", alpha=0.75)

    print("Processing Combined data")

    # Plot the combined on the last line
    axs_line = axs_grid[i + 1]

    for j, hist in enumerate(hists):
        print(f"\tPlotting {hist}")
        ax = axs_line[j]

        if j == 0:
            ax.text(-0.5, 0.5, "Combined", transform=ax.transAxes, fontsize=12)

        type = hist.split("_")[0]
        hist_type = hist.split("_")[1]
        datafile = f"data/{type}_data_hist/comb"
        cols = columns_by_type[type]
        df = pd.read_csv(datafile, names=cols)

        if "rw" in cols:
            # Plot double histos for R and W separately
            ax.hist(df[df["rw"] == "R"][hist_type], bins=50, color="orange", alpha=0.75)
            ax.hist(df[df["rw"] == "W"][hist_type], bins=50, color="blue", alpha=0.75)
        else:
            ax.hist(df[hist_type], bins=50, color="green", alpha=0.75)

    fig.suptitle("MLCommons Image Segmentation")
    plt.savefig("./plots/histograms/all.png", format="png", dpi=600)


def plot_histograms_RW(log_counts=False):
    pids = [
        "1313298",
        "1313302",
        "1313336",
        "1313402",
        "1313403",
        "1313404",
        "1313405",
        "1313406",
        "1313407",
        "1313408",
        "1313409",
        "comb",
    ]

    hists = [
        "bio_lat",
        "bio_size",
        "open_lat",
        "vfsopen_lat",
        "vfsrw_lat",
        "vfsrw_sizereq",
        "vfsrw_sizeret",
    ]

    hists_pretty_titles = {
        "bio_lat": ["BIO", "Latencies"],
        "bio_size": ["BIO", "Sizes"],
        "open_lat": "openat() Latencies",
        "vfsopen_lat": "vfs_open() Latencies",
        "vfsrw_lat": ["VFS", "Latencies"],
        "vfsrw_sizereq": ["VFS", "Sizes Requested"],
        "vfsrw_sizeret": ["VFS", "Sizes Returned"],
    }

    columns_by_type = {
        "bio": ["rw", "lat", "size"],
        "open": ["lat"],
        "vfsopen": ["lat"],
        "vfsrw": ["rw", "lat", "sizereq", "sizeret"],
    }

    hists_in_bytes = ["size", "sizereq", "sizeret"]

    #
    # Plot PIDs
    #
    for pid in pids:
        print(f"Processing pid {pid}")

        folder = "./plots/histograms/indiv/"

        if log_counts:
            folder += "log_counts/"

        for hist in hists:

            type = hist.split("_")[0]
            hist_type = hist.split("_")[1]

            if pid == "comb":
                datafile = f"data/{type}_data_hist/comb"
            else:
                datafile = f"data/{type}_data_hist/hist_{type}_{pid}"

            cols = columns_by_type[type]
            df = pd.read_csv(datafile, names=cols)

            x_label = "Size (B)" if hist_type in hists_in_bytes else "Latency (ns)"

            if "rw" in cols:
                # Plot individual histograms for R and W
                for rw in ["R", "W"]:
                    print(f"\tPlotting {hist} {rw}")

                    if df[df["rw"] == rw][hist_type].size == 0:
                        print("\t\tNo data, skipping")
                        continue

                    fig, ax = plt.subplots(figsize=(10, 10))

                    ax.set_xlabel(x_label)
                    title = hists_pretty_titles[hist]
                    ax.grid(True, linestyle="--", linewidth=0.2, color="grey", alpha=0.25)
                    ax.set_title(
                        f"{pid}: {title[0]} {'Write' if rw == 'W' else 'Read'} {title[1]}"
                    )

                    color = "coral" if rw == "W" else "royalblue"
                    ax.hist(df[df["rw"] == rw][hist_type], bins=100, color=color, alpha=0.75)

                    if log_counts:
                        ax.set_yscale("log")
                        ax.set_ylabel("Log counts")
                    else:
                        ax.set_ylabel("Counts")

                    outname = folder + f"{pid}_{hist}_{rw}.png"
                    plt.savefig(
                        outname,
                        format="png",
                        dpi=600,
                    )
                    plt.close()
            else:
                print(f"\tPlotting {hist}")

                if df[hist_type].size == 0:
                    print("\t\tNo data, skipping.")
                    continue

                fig, ax = plt.subplots(figsize=(10, 10))
                ax.set_xlabel(x_label)
                ax.grid(True, linestyle="--", linewidth=0.2, color="grey", alpha=0.25)

                ax.hist(df[hist_type], bins=100, color="lime", alpha=0.75)
                ax.set_title(f"{pid}: {hists_pretty_titles[hist]}")

                if log_counts:
                    ax.set_yscale("log")
                    ax.set_ylabel("Log counts")
                    outname = f"./plots/histograms/v2/log/{pid}_{hist}.png"
                else:
                    ax.set_ylabel("Counts")
                    outname = f"./plots/histograms/v2/{pid}_{hist}.png"

                plt.savefig(outname, format="png", dpi=600)
                plt.close()


if __name__ == "__main__":
    # plot_histograms_pids()
    plot_histograms_RW()
    plot_histograms_RW(log_counts=True)
