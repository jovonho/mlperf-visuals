#!/bin/bash


# Create folders to house files
if [[ ! -d ./bio_data ]]
then
    echo "Creating output directory bio_data"
    mkdir bio_data
fi

if [[ ! -d ./open_data ]]
then
    echo "Creating output directory open_data"
    mkdir open_data
fi

if [[ ! -d ./vfsrw_data ]]
then
    echo "Creating output directory vfsrw_data"
    mkdir vfsrw_data
fi

if [[ ! -d ./vfsopen_data ]]
then
    echo "Creating output directory vfsopen_data"
    mkdir vfsopen_data
fi


# Extract lines containing "python" from the bio trace, since it captured bio for all processes. 
# Note: this will include lines where python is the return probe context command (i.e column DONECOMM)
grep -a "python" bio_time_aligned.out > bio_python.out

# Extract unique PIDs from python processes
# python3 processes are unrelated so exclude them
awk -F ' ' '{print $2,$3}' bio_python.out | grep -v "python3" | grep -a "python" | awk -F ' ' '{print $1}' | sort -u > unique_pids

# Use the PIDs to extract their lines from each trace
while read pid; do
    # Remove whitespaces and newlines from pid
    pid=${pid//[$'\t\r\n']}
    echo "Processing $pid"

    # Block IO trace
    # Extract the pid's lines from the trace, remove less relevant columns
    # We're keepin only timestamp, pid, r/w, sector, req size, latency.
    grep -a " $pid " bio_python.out | awk -F '\\s+' '{print $1,$2,$7,$8,$9,$10}' > "bio_data/bio_$pid"
    # Note: Need spaces in the grep else we get random lines where timestamp matches the pid 

    # Open trace (openat part)
    grep -a " $pid " open_time_aligned.out | grep -a "openat" | awk -F ' ' '{print $1,$2,$4,$5,$6}' > "open_data/open_$pid"

    # Open trace (VFS open part)
    grep -a " $pid " open_time_aligned.out | grep -a "vfs_open" | awk -F ' ' '{print $1,$2,$4,$5,$6}' > "vfsopen_data/vfsopen_$pid"

    # VFS R/W trace
    grep -a " $pid " vfs_rw_time_aligned.out | awk -F ' ' '{print $1,$2,$4,$5,$6,$7,$8}' > "vfsrw_data/vfsrw_$pid"

done < ./unique_pids
