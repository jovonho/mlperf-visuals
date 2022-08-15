

# Preprocessing the raw data

Note: this code was written specifcally for the image segmentation traces and logs. It WILL need to be adapted to visualize other workloads, esp. DLIO. 

The main steps in adapting this code to other workloads will be in parsing the different application log and outputting correct events (i.e. epoch start, epoch end, etc.) and understanding which PIDs to plot and what they correspond to. Read below to understand where those changes should be made.

## Generate plot from the test data

There are some real traces in `data/4gpu_test_data.tar.gz` so you can generate the plots for it and understand the codebase.
After uncompressing the data and placing the resulting folder in `data/`:

1) Navigate inside the `data` directory then run `preprocess_traces.sh` with the correct arguments. There are some path issues if you try running the script from elsewhere.
This will prepare the raw data for plotting into a timeline visualization.

2) From the root directory, run `timeline.py` to generate the plots. The script will read the event information and generate an overview plot as well as zooms into various points of interest.

3) The plotting script will crash with an error that you will have to fix as an exercise ;). These happen often as the traces don't always have perfectly formatted output / weird things happen.

## Proprocessing pipeline steps

`preprocess_traces.sh` launches the following scripts in sequence:
1. `align_time.py` goes through the time alignment trace to estimate an alignment of bpftrace 'nsecs since boot' timestamps to UTC time, and rewrites the traces with UTC timestamps.
2. `pid_names.py` parses the PID trace to generate a map of `PID -> name` for plotting. This script was used for plotting image segmentation and is specific to pytorch and the different ways to launch that workload on multiple GPUs. **This will have to be modified to plot the other workloads and DLIO, and will require some analysis first to understand which processes do what**.
3. `split_traces_by_pid.sh` splits the traces, creating one for each PID. 
4. `prepare_traces_for_timelines.sh` for each PID, combines the read, write, open and bio traces, keeping only necessary fields and calls `ts_to_start_end.py` to convert the trace format from `<start timestamp> <event> <duration>` to `<start timestamp> <end timestamp> <event>` . 
5. `cpu.sh`, `gpu.sh` and `cpu_gpu.py` which process the CPU and GPU traces, extracting only the 'all' line of the CPU trace and calculating the average of all GPUs. 
6. `mllog.sh` and `mllog_UNIX_to_UTC_ts.py` which clean up the image segmentation app log and output a `<start timestamp> <end timestamp> <event>` formatted trace of important logical events of training (initialization, epoch start and end, evaluation), converting unix timestamps of the app logs to UTC. **These scripts will also need to be modified and adapted to other workloads as the application log might be structured differently/have different logical events. DLIO will even need to be modified to output some timestamped log as it does not do so currently.** 


There are other processing scripts to plot histograms and various utilities that can be useful for you to discover.

<br>

### Adding a new trace

If you define a new trace, you must add it to the TRACES array at the start of `align_time.py` and extend the various scripts under `data` to account for it during preprocessing.


<br>

### Old documentation
----------------------
There are many different scripts in here that need to be run in a specific order to work.

The main plotting ones are in the root directory, but we first need to run the preprocessing ones in the `data/` folder.
Depending on if you ran your traces on a machine with GPUs, which logging library was used, how many worker processes were run, etc., you may not need to run some of them or create new ones. 

1) Follow steps in `data/align_time_README.md` to approximately align the nsecs since boot timestamp with local time.

2) Write the estimated alignment in `align_time.py` and run the script to create UTC timestamps for each trace. 

3) If you notice some very large negative latencies in your vfsrw trace, run `vfsrw_bugfix.py` to fix them. It is due to an integer overflow error, but we can recover the original value. 

4) Run `split_traces_by_pid.sh` to split the now time aligned traces by PID.

5) Now run `prepare_traces_for_timelines.sh` which will create a new file for each PID in a convenient format for plotting timelines. This script will invoke `ts_to_start_end.py` which will take the UTC timestamps and the latency of each traced operation to create a start and end timestamp for each line in the traces. 

6) Run `cpu.sh` to extract individual CPU data (we only really need the cpu.all trace however)

7)  Open `cpu_all.py` and change the date in the script before running it.

8)  If you have a gpu.out trace, run `gpu.sh` and `gpu_avg.py`

9)  If you ran an mllog workload, run `mllog.sh` to extract timeline info followed by `mllog_UNIX_to_UTX_ts.py` to convert the UNIX timsetamps to UTC timestamps.

10) Now all the data is preprocessed and you can run `plot_timelines.py` to create the timeline plots (look in the main function, you may have to change some stuff)