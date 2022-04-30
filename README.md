
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