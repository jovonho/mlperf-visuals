#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: $0 <traces meta dir>" 
done

datadir=$1
parent_dir=$(dirname $1)

for d in $(ls $datadir | grep -v ta_)
do
	echo $d
    num_gpus=${d:0:1}
	tmux kill-session -t $d
	tmux new-session -d -s $d
	tmux send-keys -t $d "./pp_and_plot.sh ${parent_dir}/${d} $num_gpus" C-m
done
