Probes/Scripts can be found here (branch DGX1_v2): https://github.com/jovonho/mlperf-traces/tree/dgx1_v2

The versions on github are not the exact ones that generated the traces. I forgot to push the actual versions and have since lost them.
However, they were mostly the same with differences mostly in the filters used (e.g. tracing only comm=="python" processes for the
vfs_read/write and open traces. I am also missing the launch scripts for the non bpftrace traces, like CPU (mpstat) and GPU usage (nvidia-smi).
I'll make sure this doesn't happen again in future tracing! :)

Some preliminary notes:
- The MLPerf image segmentation workload was run on a DGX-1 machine, and parallelized to use the 8 GPUs (used 1 by default).
- Before training, a data pre-processing script is run which takes the raw data and saves a numpy formatted file for each x and y
sample. The training uses the pre-procesed data only.
- While the raw data was placed on nfs, the pre-processed data was placed on the sda disk. It's unclear to me what block IO activity would
be observed in the traces if it was on nfs, so this was a precaution.
- The first version of these traces could not find any disk reads. This was due to the filesystem caching the pre-procesed data,
given its relatively small size (~30 GB). This was fixed by running `sync; echo 3 > /proc/sys/vm/drop_caches` before starting.

Bugs:
- There is an integer overflow in some latency measures in the VFSRW trace. 
We correct these by converting to the unsigned integer.

Analysis:

- We see no Block IO Writes initiated in python context (i.e. `grep [0-9]{9} [0-9]{7} python 1` returns empty) but we know that 
we are at least writing to the log file. We see some BIO writes in other contexts that could be associated with these. 

- The 4th most frequent written file is anonymous. 
We get the filname using ((struct file *)arg0)->f_path.dentry->d_name.name. 

Write activity:
    1313336 writes the most to the anon file and writes to the most /dev/shm files

    1313402 does the vast majority of logging (writes to unet3d.log and stdout) and does all the json.log writing
    other workers have similar write activity

Intersting times for writes:

    20:27:44 336 writes to the /dev/shm files and the anon file 
        - observe that a cascade of opening occurs in the workers
        
    20:27:49 workers write to [eventfd]

    20:27:53-54 402 does its first batch of logging, then every ~20sec does more logging

    18:41:45 all workers write to anon file
    2022-02-06T18:41:47 336 has more write acitivty to anon file


About /dev/shm:
All the opened shared memory files can be found in data/writes/vfs_writes/all_shm_files.

About log.json: Looks like each worker thread opens it

2022-02-05T20:27:46.077425393 1313403 python vfs_open 100226 log.json
2022-02-05T20:27:46.077482950 1313403 python openat 164906 /tmp/log.json
2022-02-05T20:27:46.077425714 1313408 python vfs_open 102177 log.json
2022-02-05T20:27:46.077474865 1313408 python openat 572281 /tmp/log.json
2022-02-05T20:27:46.078082623 1313404 python vfs_open 17219 log.json
2022-02-05T20:27:46.078118929 1313404 python openat 60117 /tmp/log.json
2022-02-05T20:27:46.083798875 1313405 python vfs_open 5978 log.json
2022-02-05T20:27:46.083820114 1313405 python openat 43743 /tmp/log.json
2022-02-05T20:27:46.084489828 1313402 python vfs_open 23290 log.json
2022-02-05T20:27:46.084523736 1313402 python openat 63159 /tmp/log.json
2022-02-05T20:27:46.084587269 1313406 python vfs_open 30573 log.json
2022-02-05T20:27:46.084622121 1313406 python openat 56000 /tmp/log.json
2022-02-05T20:27:46.085215992 1313407 python vfs_open 7825 log.json
2022-02-05T20:27:46.085237414 1313407 python openat 38660 /tmp/log.json
2022-02-05T20:27:46.100537623 1313409 python vfs_open 22696 log.json
2022-02-05T20:27:46.100554095 1313409 python openat 62466 /tmp/log.json


TRACES:

================================================
bio.out
Uses the two kernel probes blk_account_io_start() and blk_account_io_done() to trace block IO requests.
We are able to map the start and end probes by using the address of the associated request as a key.
-------------------------------------------------------------------
TIMESTAMP: 		nsecs since boot
TIME:			local time
PID: 			process pid
COMM: 			process name
DONEPID:		PID of process in whose context the blk_account_io_done probe executes. (See note 1)
DONECOMM: 		name of process with above PID
DISK: 			always sda since I filtered for it.
T: 			    request type. 1 = Write, 0 = Read.
SECTOR: 		disk sector requested (__sector field of struct request in blk_account_io_start call)
BYTES: 			size of requested data (__data_len field of struct request in blk_account_io_start call)
LAT(ns):		difference btw timestamp of blk_account_io_start and blk_account_io_done calls

Note 1: In Brendan Gregg's book BPF Performance Tools we read the following at the end of 9.3.2:
"The blk_account_io_start() function often fires in process context and occurs when the I/O is queued. Later events,
such as issuing the I/O to the device and I/O completion, may or may not happen in process context, so you cannot rely
on the value of the pid and comm builtins at those later times. The solution is to store them in BPF maps during
blk_account_io_start(), keyed by the request ID, so that they can be retrieved later."
This hints that even the start probe does not always start in process context, which was observed during other experiments.
Ref: https://books.google.ca/books?id=ihTADwAAQBAJ&pg=PT517&lpg=PT517&dq=kprobe+blk+account+io+start&source=bl&ots=bzNO7FBELg&sig=ACfU3U01-3q4b5y3gileFgY7YvY8mJcCdQ&hl=en&sa=X&ved=2ahUKEwiEvu2m9Oj1AhU2jYkEHeVlBR4Q6AF6BAgJEAM#v=onepage&q&f=false


================================================
open.out
traces calls to the openat() syscall using the sys_enter_openat() and sys_exit_openat() tracepoints, and the
vfs_open() kernel function using its associated kernel probe and return kernel probe (kretprobe).

We are more interested in the vfs_open() calls here, but could only get the filename from its
kprobe, which is why we also trace openat() which gives the full path (though truncated to 63 chars) (notes 2, 3).
The full path will also be useful to understand subsequent vfs_read/write() calls.

Looking in kernel source (https://elixir.bootlin.com/linux/latest/source/fs/open.c#L1196,
https://elixir.bootlin.com/linux/latest/source/fs/namei.c#L3382)
it looks like open and openat both go through the following call sequence:
do_sys_openat2, do_filp_open, path_openat, do_open|do_tmpfile|do_opath, vfs_open.

Since the traces are printed on the return of openat and vfs_open we expect to see the vfs_open trace line
before the openat trace for the same file and the latency of openat should always be larger than that of vfs_open.
-------------------------------------------------------------------
TIMESTAMP:		nsecs since boot
TIME:			local time
PID:			process pid
COMM:			process name
FUNC:			openat or vfs_read
LAT (ns)		call latency in nsecs (difference btw the timestamps of enter and exit tracepoints or kprobe and kretprobe)
FILE			opened file (full name for openat, filename for vfs_open) (note 4)

Note 2: We only need trace openat() and not the open() syscall because "In modern Linux systems (glibc >= 2.26)
the open wrapper always calls the openat syscall."
(src: Lesson 3 - https://github.com/iovisor/bpftrace/blob/master/docs/tutorial_one_liners.md)

Note 3: In the case of openat() calls on symlinks, openat() will show the symlink name and vfs_open will the linked file name.

Note 4: For openat(), it is given in the arguments ot the tracepoint. For vfs_read, it's obtained by doing
`(struct path *)arg0)->dentry->d_name.name`. More recent versions of bpftrace have a builtin path() function which takes
a struct path as argument and print the full path, but I could not compile these newer versions to the target machine.


================================================
vfs_rw.out
Traces calls to vfs_read() and vfs_write() kernel functions using kprobes.
See https://elixir.bootlin.com/linux/latest/source/fs/read_write.c#L461 for function definitions
-------------------------------------------------------------------
TIMESTAMP: 		nsecs since boot
TIME:			local time
PID:			process pid
COMM:			process name
R/W: 			R=vfs_read, W=vfs_write
LAT (ns):		timsetamp difference between kprobe and kretprobe
REQUESTED:		number of bytes requested (arg2 or vfs_read and vfs_write calls)
RETURNED:		number of bytes read/written (return value of function)
FILE:			filename


================================================
unet3d.log
Log of the workload (uses mlperf_logging module). Has UNIX timestamps.


================================================
gpu.out
Output of `nvidia-smi pmon` showing GPU usage metrics every second.
Column definition is not 100% certain as the output of pmon is not precisely detailed in the ref.
Ref: https://developer.download.nvidia.com/compute/DCGM/docs/nvidia-smi-367.38.pdf
-------------------------------------------------------------------
Date:		YYYYMMDD
Time:		HH:MM:SS
gpu:		index of GPU (0 to 7)
pid:		process using the GPU
type: 		Type of the process. C=Compute, G=Graphics. Always C in this case.
sm:			% of time over the past sample period during which one or more kernels was executing on the GPU. (SM = Streaming Multiprocessor = GPU processor) 
mem:		% of time over the past sample period during which global (device) memory was being read or written. 
enc:  		% of time over the past sample period during which the GPU's video encoder was being used.
dec:  		% of time over the past sample period during which the GPU's video decoder was being used.
fb:			Frame Buffer memory usage in MB.
command:    name of program

Note 5: For future traces, `nvidia-smi dmon` might be preferable as it gives more detailed output.


================================================
cpu.out
Output of mpstat showing CPU usage metrics every second.
Ref: https://linux.die.net/man/1/mpstat
-------------------------------------------------------------------
Time:		HH:MM:SS
CPU:		CPU index or 'all' for average values
%usr:		% of CPU use that occurred while executing at the user level (application)
%nice: 		% of CPU use that occurred while executing at the user level with nice priority.
%sys:		% of CPU use that occurred while executing at the system level (kernel). This does not include time spent servicing hardware and software interrupts.
%iowait:	% of time that the CPU or CPUs were idle during which the system had an outstanding disk I/O request.
%irq:		% of time spent by the CPU or CPUs to service hardware interrupts.
%soft:		% of time spent by the CPU or CPUs to service software interrupts.
%steal:		% of time spent in involuntary wait by the virtual CPU or CPUs while the hypervisor was servicing another virtual processor.
%guest:		% of time spent by the CPU or CPUs to run a virtual processor.
%gnice:		% of time spent by the CPU or CPUs to run a niced guest.
%idle:		% of time that the CPU or CPUs were idle and the system did not have an outstanding disk I/O request.


EXTRA:

================================================
pids.out
Output of `ps aux | grep python` right after launching training, and after training has actually started.

================================================
strace_2min.out
Output of strace during the first two minutes of training. I believe this was run on the DISCS lab server.
I was trying to look at the mmap-ing being done. Still have to dig deeper into that.
