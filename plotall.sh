#!/bin/bash

for d in $(ls data/results | grep ta_)
do
	echo $d
	tmux kill-session -t $d
	tmux new-session -d -s $d
	tmux send-keys -t $d "python3 timeline.py data/results/${d} data/results/${d}/pids.json ${d} ${d}" C-m
done
