#!/bin/bash


# Determine which python command to use depending on platform 
# I run this on both windows and linux machines
unameOut="$(uname -s)"
case "${unameOut}" in
    MINGW*)     py=py;;
    *)          py=python3;;
esac

if [ $# -lt 2 ]
then
    echo "Usage: $0 traces_dir num_gpus"
    exit -1
fi

traces_dir=$1
ta_outdir="ta_$1"
mkdir -p $ta_outdir

num_gpus=$2

# Run the time alignment script on the traces
${py} align_time.py $traces_dir $ta_outdir

# Check for integer overflows in the read trace
if [[ $(grep -a "\s+\-[0-9]\s+" ${ta_outdir}/read_time_aligned.out) ]]
then 
    echo "Found some large negative values in the read() trace."
    echo "Perform integer overflow fix"
    ${py} vfsrw_bugfix.py $ta_outdir/read_time_aligned.out
fi

./split_traces_by_pid.sh $ta_outdir
./prepare_traces_for_timelines.sh $ta_outdir

# Process the CPU and GPU traces
./cpu.sh $traces_dir/cpu.out $ta_outdir
./gpu.sh $traces_dir/gpu.out $ta_outdir 
${py} cpu_gpu.py $ta_outdir/gpu_data/gpu.all $ta_outdir/cpu_data/cpu.all $num_gpus

# Process the app log
./mllog.sh $traces_dir/unet3d.log $ta_outdir
${py} mllog_UNIX_to_UTC_ts.py $ta_outdir/mllog_data/

