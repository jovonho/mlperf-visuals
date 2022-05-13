from black import out
from matplotlib import pyplot as plt, patches as mpatches, ticker
import os
import pathlib
import pandas as pd


def plot_all_hists(pids, pid_names, hists, datadir, title, filename, hists_pretty_titles = None, log_counts=False):
    
    # Create a axes grid for our plots
    fig, axs_grid = plt.subplots(
        nrows=len(pids), ncols=len(hists), figsize=(30, len(pids) * 3), sharex="col", 
    )

    columns_by_type = {
        "bio": ["r", "size", "lat"],
        "open": ["lat"],
        "read": ["r", "lat", "size"],
    }

    hists_in_bytes = ["size"]

    colors_dict = {"R": "royalblue", "W": "crimson", "NA": "purple"}

    #
    # Plot PIDs
    #
    for i, pid in enumerate(pids):

        if pid == "combined":
            continue

        print(f"Processing pid {pid}")
        axs_line = axs_grid[i]

        for j, hist in enumerate(hists):
            print(f"\tPlotting {hist}")
            ax = axs_line[j]

            # Print titles for the first line
            if i == 0:
                if hists_pretty_titles is not None:
                    ax.set_title(hists_pretty_titles[hist])
                else:
                    ax.set_title(hist)

            if j == 0:
                ax.text(-0.5, 0.5, pid_names[pid], transform=ax.transAxes, fontsize=12)
                if log_counts:
                    ax.set_ylabel("Log counts")
                else:
                    ax.set_ylabel("Counts")

            if log_counts:
                ax.set_yscale("log")

            # Plot legend
            if i == (len(pids) // 2) and j == 6:
                patches = [
                    mpatches.Patch(color=color, label=key) for (key, color) in colors_dict.items()
                ]
                ax.legend(handles=patches, bbox_to_anchor=(1, 0.5), loc="center left")

            type = hist.split("_")[0]
            hist_type = hist.split("_")[1]
            datafile = f"{datadir}/{type}_hist/hist_{type}_{pid}"
            cols = columns_by_type[type]
            df = pd.read_csv(datafile, names=cols)

            # place a text box in upper left in axes coords with the sample size
            text = f"N = {df.shape[0]}"
            props = dict(boxstyle='round', facecolor="white", alpha=0.5)
            ax.text(0.80, 0.97, text, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=props)

            ax.hist(df[hist_type], bins=50, color=colors_dict["NA"], alpha=0.75)


    print("Processing Combined data")

    # Plot the combined on the last line
    axs_line = axs_grid[i]

    for j, hist in enumerate(hists):
        print(f"\tPlotting {hist}")
        ax = axs_line[j]

        if j == 0:
            ax.text(-0.5, 0.5, "Combined", transform=ax.transAxes, fontsize=12)

            if log_counts:
                ax.set_ylabel("Log counts")
            else:
                ax.set_ylabel("Counts")

        if log_counts:
            ax.set_yscale("log")

        type = hist.split("_")[0]
        hist_type = hist.split("_")[1]
        datafile = f"{datadir}/{type}_hist/combined"

        cols = columns_by_type[type]
        df = pd.read_csv(datafile, names=cols)

        x_label = "Size (B)" if hist_type in hists_in_bytes else "Latency (ns)"
        ax.set_xlabel(x_label)

        # place a text box in upper left in axes coords with the sample size
        text = f"N = {df.shape[0]}"
        props = dict(boxstyle='round', facecolor="white", alpha=0.5)
        ax.text(0.80, 0.97, text, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=props)

        ax.hist(df[hist_type], bins=50, color=colors_dict["NA"], alpha=0.75)


    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(filename)
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    fig.suptitle(title)
    plt.savefig(filename, format="png", dpi=600)


def plot_individual_hists(pids, pid_names, hists, datadir, title, outdir, log_counts=False, log_x=False):

    hists_pretty_titles = {
        "bio_lat": ["BIO Read", "Latencies"],
        "bio_size": ["BIO Read", "Sizes"],
        "open_lat": ["open()", "Latencies"],
        "read_lat": ["read()", "Latencies"],
        "read_size": ["read()", "Sizes"],
    }

    columns_by_type = {
        "bio": ["size", "lat"],
        "open": ["lat"],
        "read": ["lat", "size"],
    }

    hists_in_bytes = ["size"]

    # Create output directory if it doesn't exist
    if log_counts and log_x:
        outdir = os.path.join(outdir, "loglog")
    elif log_counts:
        outdir = os.path.join(outdir, "log_counts")
    
    else:
        outdir = os.path.join(outdir, "counts")

    pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)

    #
    # Plot PIDs
    #
    for pid in pids:
        print(f"Processing pid {pid}")

        for hist in hists:

            type = hist.split("_")[0]
            hist_type = hist.split("_")[1]

            if pid == "combined":
                datafile = f"{datadir}/{type}_hist/combined"
            else:
                datafile = f"{datadir}/{type}_hist/hist_{type}_{pid}"

            cols = columns_by_type[type]
            df = pd.read_csv(datafile, names=cols)

            x_label = "Size (B)" if hist_type in hists_in_bytes else "Latency (ns)"

            text = f"N = {df.shape[0]}"
            # these are matplotlib.patch.Patch properties
            props = dict(boxstyle='round', facecolor="white", alpha=0.5)

            if "rw" in cols:
                # Plot individual histograms for R and W
                for rw in ["R", "W"]:
                    print(f"\tPlotting {hist} {rw}")

                    if df[df["rw"] == rw][hist_type].size == 0:
                        print("\t\tNo data, skipping")
                        continue

                    fig, ax = plt.subplots(figsize=(10, 10))

                    
                    title = hists_pretty_titles[hist]
                    ax.grid(True, linestyle="--", linewidth=0.2, color="grey", alpha=0.25)
                    ax.set_title(
                        f"{pid_names[pid]}: {title[0]} {'Write' if rw == 'W' else 'Read'} {title[1]}"
                    )

                    color = "coral" if rw == "W" else "royalblue"
                    ax.hist(df[df["rw"] == rw][hist_type], bins=100, color=color, alpha=0.75)
                    # place a text box in upper left in axes coords
                    ax.text(0.83, 0.97, text, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)

                    locator = ticker.LinearLocator(numticks=None, presets=None)
                    ax.xaxis.set_major_locator(locator)

                    if log_counts:
                        ax.set_yscale("log")
                        ax.set_ylabel("Log counts")
                    else:
                        ax.set_ylabel("Counts")

                    if log_x:
                        ax.set_xscale("log")
                        ax.set_xlabel(f"Log {x_label}")
                    
                    fig.suptitle(title)
                    plt.savefig(
                        os.path.join(outdir, f"{pid}_{hist}_{rw}.png"),
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

                ax.hist(df[hist_type], bins=100, color="purple", alpha=0.75)
                ax.set_title(f"{pid_names[pid]}: {' '.join(hists_pretty_titles[hist])}")
                # place a text box in upper left in axes coords
                ax.text(0.83, 0.97, text, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
                # locator = ticker.LinearLocator(numticks=None, presets=None)
                # ax.xaxis.set_major_locator(locator)

                if log_counts:
                    ax.set_yscale("log")
                    ax.set_ylabel("Log counts")
                else:
                    ax.set_ylabel("Counts")

                if log_x:
                    ax.set_xscale("log")
                    ax.set_xlabel(f"Log {x_label}")

                fig.suptitle(title)
                plt.savefig(os.path.join(outdir, f"{pid}_{hist}.png"), format="png", dpi=600)
                plt.close()


if __name__ == "__main__":

    # Histograms you want to plot
    hists = [
        "bio_lat",
        "bio_size",
        "open_lat",
        "read_lat",
        "read_size",
    ]

    hists_pretty_titles = {
        "bio_lat": "BIO Read Latencies",
        "bio_size": "BIO Read Sizes",
        "open_lat": "open() Latencies",
        "read_lat": "read() Latencies",
        "read_size": "read() Sizes",
    }

    DATA_DIR = "data/4gpus_1xRAM"

    pids = [
        # "32260",       # Possibly just loading the mllog library
        # "32261",
        "33677",        # Main process
        # "32264",
        "33710",        # Multiprocessing resource tracker
        "33711",        # Workers 
        "33712",
        "33713",
        "33714",
        "combined"
    ]

    pid_names = {
        "33677": "master process",
        "33710": "resource tracker", 
        "33711": "worker 1",        
        "33712": "worker 2",
        "33713": "worker 3",
        "33714": "worker 4",
        "combined": "combined"
    }

    
    title = "Image Segmentation - 4 GPUs 1xRAM"

    plot_all_hists(
        pids, 
        pid_names,
        hists, 
        hists_pretty_titles = hists_pretty_titles,
        datadir = DATA_DIR,
        title=title,
        filename="plots/histograms/4gpu_1xRAM_hists.png", 
        log_counts=False
    )

    plot_all_hists(
        pids, 
        pid_names,
        hists, 
        hists_pretty_titles = hists_pretty_titles,
        datadir = DATA_DIR,
        title=title,
        filename="plots/histograms/4gpu_1xRAM_hists_log.png", 
        log_counts=True
    )

    plot_individual_hists(
        pids, 
        pid_names,
        hists, 
        datadir = DATA_DIR,
        title=title,
        outdir="plots/histograms/1xRAM", 
        log_counts=True
    )

    exit(0)
    
    DATA_DIR = "data/ta_4gpus_100gb"

    pids = [
        "16910",    #master
        "16943",    # RT
        "16944",
        "16945",
        "16946",
        "16947",
        "combined"
    ]

    pid_names = {
        "16910": "master process",
        "16943": "resource tracker", 
        "16944": "worker 1",        
        "16945": "worker 2",
        "16946": "worker 3",
        "16947": "worker 4",
        "combined": "combined"
    }

    title = "Image Segmentation - 4 GPUs 100GB"

    # plot_all_hists(
    #     pids, 
    #     pid_names,
    #     hists, 
    #     hists_pretty_titles = hists_pretty_titles,
    #     datadir = DATA_DIR,
    #     title=title,
    #     filename="plots/histograms/4gpu_100gb_hists.png", 
    #     log_counts=False
    # )

    plot_all_hists(
        pids, 
        pid_names,
        hists, 
        hists_pretty_titles = hists_pretty_titles,
        datadir = DATA_DIR,
        title=title,
        filename="plots/histograms/4gpu_100gb_hists_log.png", 
        log_counts=True
    )

    # plot_individual_hists(
    #     pids, 
    #     pid_names,
    #     hists, 
    #     datadir = DATA_DIR,
    #     title=title,
    #     outdir="plots/histograms/100gb", 
    #     log_counts=False
    # )

    # plot_individual_hists(
    #     pids, 
    #     pid_names,
    #     hists, 
    #     datadir = DATA_DIR,
    #     title=title,
    #     outdir="plots/histograms/100gb", 
    #     log_counts=True
    # )


# 2xRAM
# +REF_TIMESTAMP = 104994782256577
# +REF_LOCALTIME = np.datetime64("2022-04-29T22:40:37.000000000")

# 1xRAM
# 75530751851216 2022-04-29T14:29:33.000000000

   
