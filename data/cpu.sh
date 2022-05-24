#!/bin/bash

# Preproc cpu.out trace into individual CPU trace files

if [ $# -lt 2 ]
then    
    echo "Usage: $0 cpu_trace.out output_dir"
    exit -1
fi

cpu_trace=$1
output_dir=$2

if [[ ! -d $output_dir/cpu_data ]]
then
    echo "Creating output directory $output_dir/cpu_data"
    mkdir $output_dir/cpu_data
fi

grep "all" $cpu_trace > $output_dir/cpu_data/cpu.all
