#!/bin/bash


if [ $# -ne 3 ]
then
    echo "Usage: $0 traces_dir ref_ts ref_t"
    exit -1
fi

traces_dir=$1
ref_ts=$2
ref_t=$3

ta_outdir="ta_$1"
mkdir -p $ta_outdir

# Run the time alignment script on the traces
py align_time.py $traces_dir $ta_outdir $ref_ts $ref_t

# Check for integer overflows in the read trace TODO: fix the trace so this doesn't happen
if [[ $(grep -a "\s+\-[0-9]{2}\s+" ${ta_outdir}/read_time_aligned.out) ]]
then 
    echo "Found some large negative values in the read() trace."
    echo "Perform integer overflow fix"
    py vfsrw_bugfix.py $ta_outdir/read_time_aligned.out
fi

./split_traces_by_pid.sh $ta_outdir
./prepare_traces_for_timelines.sh $ta_outdir

./cpu.sh $traces_dir/cpu.out $ta_outdir
py cpu_all.py $ta_outdir/cpu_data/cpu.all

./gpu.sh $traces_dir/gpu.out $ta_outdir
py gpu_avg.py $ta_outdir/gpu_data/gpu.all

./mllog.sh $traces_dir/unet3d.log $ta_outdir
py mllog_UNIX_to_UTC_ts.py $ta_outdir/mllog_data/

# timeline_dir="timeline_data/$traces_dir"
# mkdir -p $timeline_dir

# mv cpu_data $timeline_dir
# mv gpu_data $timeline_dir
# mv st_start_end $timeline_dir