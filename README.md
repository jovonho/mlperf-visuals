
There are many different scripts in here that need to be run in a specific order to work.

The main plotting ones are in the root directory, but we first need to run the preprocessing ones in the `data/` folder.
Depending on if you ran your traces on a machine with GPUs, which logging library was used, how many worker processes were run, etc., you may not need to run some of them or create new ones. 


1) Place the traces in the `data/` directory. The scripts expect them to be called `cpu.out`, `gpu.out`, `bio.out`, `vfs_rw.out`, `open.out` and `unet3d.log` so you can either rename them or modify the scripts if they are not called that.  

2) If you notice some very large negative latencies in your vfsrw trace, run `vfsrw_bugfix.py` to fix them. It is due to an integer overflow error, but we can recover the original value. 

3) Run `merge_traces.sh`, this will create a `combined.out` file.

4) Follow steps in `data/align_time_README.md` to approximately align the nsecs since boot timestamp with local time. 

5) Write the estimated alignment in `align_time.py` and run the script to create UTC timestamps for each trace. 

6) Run `traces.sh` to split the now time aligned bio, vfs_rw and open traces by PID.

7) Now run `prepare_traces_for_timelines.sh` which will create a new file for each PID in a convenient format for plotting timelines. This script will invoke `ts_to_start_end.py` which will take the UTC timestamps and the latency of each traced operation to create a start and end timestamp for each line in the traces. 

8) Run `cpu.sh` to extract individual CPU data (we only really need the cpu.all trace however)

9) Open `cpu_all.py` and change the date in the script before running it.

10) If you have a gpu.out trace, run `gpu.sh` and `gpu_avg.py`

11) If you ran an mllog workload, run `mllog.sh` to extract timeline info followed by `mllog_UNIX_to_UTX_ts.py` to convert the UNIX timsetamps to UTC timestamps.

12) Now all the data is preprocessed and you can run `plot_timelines.py` to create the timeline plots (look in the main function, you may have to change some stuff)