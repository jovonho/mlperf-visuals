#!/bin/bash

if [[ $# -lt 1 || ! -d $1 ]]
then
    echo "Usage: $0 time_aligned_traces_dir"
    exit -1
fi

datadir=$1

# Create folders to house files
if [[ ! -d $datadir/bio_data ]]
then
    echo "Creating output directory $datadir/bio_data"
    mkdir -p $datadir/bio_data
fi

if [[ ! -d $datadir/open_data ]]
then
    echo "Creating output directory $datadir/open_data"
    mkdir -p $datadir/open_data
fi

if [[ ! -d ./read_data ]]
then
    echo "Creating output directory $datadir/read_data"
    mkdir -p $datadir/read_data
fi

if [[ ! -d $datadir/write_data ]]
then
    echo "Creating output directory $datadir/write_data"
    mkdir -p $datadir/write_data
fi


# Extract unique PIDs from each trace file, then take the unique ones
# This will ensure we will not miss a PID only appearing in one trace
for file in $(find $1 -maxdepth 1 -type f -exec echo {} +)
do
    echo "Extracting PIDs from $file"
    awk -F ' ' '{print $2,$3}' $file | awk -F ' ' '{print $1}' | sort -u >> $datadir/unique_pids_tmp
    
done

sort -u $datadir/unique_pids_tmp > $datadir/unique_pids
rm $datadir/unique_pids_tmp

# Remove empty lines
sed '/^[[:space:]]*$/d' $datadir/unique_pids

echo "PIDs extracted:"
cat $datadir/unique_pids

# Use the PIDs to extract their lines from each trace
while read pid; do
    # Remove whitespaces and newlines from pid
    pid=${pid//[$'\t\r\n']}
    echo "Processing $pid"

    # Block IO trace
    # Extract the pid's lines from the trace, remove less relevant columns
    # We're keeping only timestamp, pid, r/w, sector, req size, latency.
    grep -a " $pid " $1/bio_time_aligned.out | awk -F '\\s+' '{print $1,$2,$7,$8,$9,$10}' > "$datadir/bio_data/bio_$pid"

    grep -a " $pid " $1/openat_time_aligned.out | awk -F ' ' '{print $1,$2,$4,$5,$6}' > "$datadir/open_data/open_$pid"

    grep -a " $pid " $1/read_time_aligned.out | awk -F ' ' '{print $1,$2,$4,$5,$6}' > "$datadir/read_data/read_$pid"

    grep -a " $pid " $1/write_time_aligned.out | awk -F ' ' '{print $1,$2,$4,$8,$9}' > "$datadir/write_data/write_$pid"


done < $datadir/unique_pids
