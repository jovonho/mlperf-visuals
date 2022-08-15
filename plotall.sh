#!/bin/bash

# List all directories in the data_dir (which is assumed to hold raw traces in each dir)
# and run the preprocessing and plotting pipeline on them
if [ $# -ne 1 ]
then
    echo "Usage: $0 <data dir>" 
    exit -1
fi

dir=$1

for d in $(find $dir -type d | grep -v ta_)
do
	d=$(basename $d)
	echo $d
    num_gpus=${d:0:1}	# Extract the first digit of the trace directory - assumed ot be the number of gpus used
	tmux kill-session -t $d
	tmux new-session -d -s $d
	tmux send-keys -t $d "./pp_and_plot.sh $dir/$d $num_gpus" C-m
	echo "./pp_and_plot.sh $dir/$d $num_gpus"
done
