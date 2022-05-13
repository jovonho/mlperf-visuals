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

# for i in {0..7}
# do
#         echo "Extracting traces for GPU $i"
#         grep -E "[0-9]{8}\s+[0-9]{2}:[0-9]{2}:[0-9]{2}\s+$i.*" gpu.out > gpu_data/gpu.$i
# done

# Extract raw data only, for calculating the average more easily
grep -E "[0-9]{8}\s+[0-9]{2}:[0-9]{2}:[0-9]{2}\s+[0-9].*" $gpu_trace > $output_dir/gpu_data/gpu.all
