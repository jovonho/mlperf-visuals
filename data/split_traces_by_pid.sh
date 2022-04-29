#!/bin/bash

if [[ $# -lt 1 || ! -d $1 ]]
then
    echo "Usage: $0 time_aligned_traces_dir"
    exit -1
fi

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

if [[ ! -d ./read_data ]]
then
    echo "Creating output directory read_data"
    mkdir read_data
fi

if [[ ! -d ./write_data ]]
then
    echo "Creating output directory write_data"
    mkdir write_data
fi


# Extract unique PIDs from each trace file, then take the unique ones
# This will ensure we will not miss a PID only appearing in one trace

for file in $(ls $1)
do
    echo "Extracting PIDs from $file"
    awk -F ' ' '{print $2,$3}' $1/$file | awk -F ' ' '{print $1}' | sort -u >> unique_pids_tmp
done

sort -u unique_pids_tmp > unique_pids
rm unique_pids_tmp

echo "PIDs extracted:"
cat unique_pids

# Use the PIDs to extract their lines from each trace
while read pid; do
    # Remove whitespaces and newlines from pid
    pid=${pid//[$'\t\r\n']}
    echo "Processing $pid"

    # Block IO trace
    # Extract the pid's lines from the trace, remove less relevant columns
    # We're keeping only timestamp, pid, r/w, sector, req size, latency.
    grep -a " $pid " $1/bio_time_aligned.out | awk -F '\\s+' '{print $1,$2,$7,$8,$9,$10}' > "bio_data/bio_$pid"

    grep -a " $pid " $1/openat_time_aligned.out | awk -F ' ' '{print $1,$2,$4,$5,$6}' > "open_data/open_$pid"

    grep -a " $pid " $1/read_time_aligned.out | awk -F ' ' '{print $1,$2,$4,$5,$6}' > "read_data/read_$pid"

    grep -a " $pid " $1/write_time_aligned.out | awk -F ' ' '{print $1,$2,$4,$8,$9}' > "write_data/write_$pid"


done < ./unique_pids
