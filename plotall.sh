#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: $0 <data dir>" 
done

dir=$1
parent=$(basename $dir)

for d in $(ls $dir | grep -v ta_)
do
	echo $d
    num_gpus=${d:0:1}
	tmux kill-session -t $d
	tmux new-session -d -s $d
	tmux send-keys -t $d "./pp_and_plot.sh $dir/$d $num_gpus" C-m
done
