#!/bin/bash

if [[ ! -d ./gpu_data ]]
then
    echo "Creating output directory gpu_data"
    mkdir gpu_data
fi

for i in {0..7}
do
        echo "Extracting traces for GPU $i"
        grep -E "[0-9]{8}\s+[0-9]{2}:[0-9]{2}:[0-9]{2}\s+$i.*" gpu.out > gpu_data/gpu.$i
done

# Extract raw data only, for calculating the average more easily
grep -E "[0-9]{8}\s+[0-9]{2}:[0-9]{2}:[0-9]{2}\s+[0-9].*" gpu.out > gpu_data/gpu.raw
