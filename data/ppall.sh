#!/bin/bash

for d in $(ls results)
do
	echo $d
	tmux kill-session -t $d
	tmux new-session -d -s $d
	tmux send-keys -t $d "./preprocess_traces.sh results/${d} ${d:0:1}" C-m
done
