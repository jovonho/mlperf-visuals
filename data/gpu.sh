#!/bin/bash

if [ $# -lt 2 ]
then    
    echo "Usage: $0 gpu_trace.out output_dir"
    exit -1
fi

gpu_trace=$1
output_dir=$2


if [[ ! -d $output_dir/gpu_data ]]
then
    echo "Creating output directory $output_dir/gpu_data"
    mkdir $output_dir/gpu_data
fi

# Extract raw data only, for calculating the average more easily
# Filtering on python will extract only the gpus used for training
grep -E "python" $gpu_trace > $output_dir/gpu_data/gpu.all
