#!/bin/bash

if [ $# -lt 1 ]
then
    echo "Usage: $0 unet3d.log"
    exit -1
fi

if [[ ! -d ./mllog_data ]]
then
    echo "Creating output directory mllog_data"
    mkdir mllog_data
fi

# Remove ":::MLLOG" prefix from all ligns
sed 's/:::MLLOG //' $1 > mllog_data/u.log

# Remove empty namespace field
awk -F ', ' 'BEGIN { OFS= ", "; ORS="\n"} {$1="{"; print $0}' mllog_data/u.log > tmp && mv tmp mllog_data/u.log
sed -i 's/{, /{/' mllog_data/u.log

# Extract training timeline info 
# Note: block_start/stop and epoch_start/stop are seemingly the same (with epoch encapsulated in block however) 
# so we omit epoch_start/stop to avoid duplicates that don't add info
grep -Ea "init_start|init_stop|run_start|run_stop|epoch_start|epoch_stop|eval_start|eval_stop" mllog_data/u.log > mllog_data/timeline.log
sed -i '$ d' mllog_data/timeline.log

awk 'BEGIN { print "[" } { print $0"," }' mllog_data/timeline.log > tmp && mv tmp mllog_data/timeline.log
# Remove last comma, make valid JSON array
sed -i '$ s/.$/\n]/' mllog_data/timeline.log

# Extract just the eval accuracies
grep -a "eval_accuracy" mllog_data/u.log > mllog_data/evals.log
# Remove useless fields
awk -F ', ' 'BEGIN {OFS= ", "; ORS="\n"} {print $1,$2,$3,$4,$7}' mllog_data/evals.log > tmp && mv tmp mllog_data/evals.log
sed -i 's/}}/}/' mllog_data/evals.log

# Convert to valid JSON array
awk 'BEGIN { print "[" } { print $0"," }' mllog_data/evals.log > tmp && mv tmp mllog_data/evals.log
sed -i '$ s/.$/\n]/' mllog_data/evals.log

# Extract all other info
grep -E -v "init_start|init_stop|run_start|run_stop|block_start|block_stop|epoch_start|epoch_stop|eval_start|eval_accuracy|eval_stop" mllog_data/u.log > mllog_data/other_info.log
awk 'BEGIN { print "[" } { print $0"," }' mllog_data/other_info.log > tmp && mv tmp mllog_data/other_info.log
sed -i '$ s/.$/\n]/' mllog_data/other_info.log

