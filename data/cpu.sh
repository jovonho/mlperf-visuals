#!/bin/bash

# Preproc cpu.out trace into individual CPU trace files

if [[ ! -d ./gpu_data ]]
then
    echo "Creating output directory cpu_data"
    mkdir cpu_data
fi

grep "all" cpu.out > ./cpu_data/cpu.all

for i in {0..77}
do
    echo "Extracting for CPU $i"
    grep -E "[0-9]{2}:[0-9]{2}:[0-9]{2}\s+$i.*" cpu.out > ./cpu_data/cpu.$i
done