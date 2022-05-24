#!/bin/bash

# Determine the python executable to call
unameOut="$(uname -s)"
case "${unameOut}" in
    MINGW*)     py=py;;
    *)          py=python3;;
esac


if [[ $# -ne 1 ]]
then
    echo "Usage: $0 output_dir"
    exit -1
fi

outdir=$1

# Create folders to house files
if [[ ! -d $outdir/traces_data ]]
then
    echo "Creating output directory $outdir/traces_data"
    mkdir -p $outdir/traces_data
fi

# For each unique PID, combine the bio, open and vfsrw traces
# print out relevant columns in a way that will make plotting easier
while read pid; do
    # Remove whitespaces and newlines from pid
    pid=${pid//[$'\t\r\n']}
    outfile="$outdir/traces_data/comb_$pid"

    echo "Writing $outfile"
    bio="$outdir/bio_data/bio_$pid"
    open="$outdir/open_data/open_$pid"
    read="$outdir/read_data/read_$pid"
    write="$outdir/write_data/write_$pid"

    # Handle the different traces, we will keep only the timestamp, type and latency here
    echo -e "\tbio"
    awk -F ' ' '{printf $1","; if ($3=="R") printf "BIOR,"; else printf "BIOW,"; printf $5"\n";}' $bio > bio_tmp

    echo -e "\topen"
    awk -F ' ' '{printf $1",OPENAT,"$3"\n";}' $open > open_tmp

    echo -e "\tread"
    awk -F ' ' '{printf $1",READ,"$4"\n";}' $read > read_tmp

    echo -e "\twrite"
    awk -F ' ' '{printf $1",WRITE,"$4"\n";}' $write > write_tmp


    # Merge the traces into one, sort
    cat bio_tmp open_tmp read_tmp write_tmp > $outfile
    sort -o $outfile $outfile

    # Transform timestamps and latency into start and end dates for plotting
    ${py} ts_to_start_end.py $outfile

done < $outdir/unique_pids

# Cleanup
rm bio_tmp open_tmp read_tmp write_tmp