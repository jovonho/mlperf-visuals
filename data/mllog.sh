#!/bin/bash

if [ $# -lt 2 ]
then
    echo "Usage: $0 unet3d.log output_dir"
    exit -1
fi

logfile=$1
output_dir=$2

if [[ ! -d $output_dir/mllog_data ]]
then
    echo "Creating output directory $output_dir/mllog_data"
    mkdir $output_dir/mllog_data
fi

output_dir=$output_dir/mllog_data

# Remove ":::MLLOG" prefix from all ligns
sed 's/:::MLLOG //' $logfile > $output_dir/u.log

# Remove empty namespace field
awk -F ', ' 'BEGIN { OFS= ", "; ORS="\n"} {$1="{"; print $0}' $output_dir/u.log > tmp && mv tmp $output_dir/u.log
sed -i 's/{, /{/' $output_dir/u.log

# Extract training timeline info 
# Note: block_start/stop and epoch_start/stop are seemingly the same (with epoch encapsulated in block however) 
# so we omit epoch_start/stop to avoid duplicates that don't add info
grep -Ea "init_start|init_stop|run_start|run_stop|epoch_start|epoch_stop|eval_start|eval_stop" $output_dir/u.log > $output_dir/timeline.log
sed -i '$ d' $output_dir/timeline.log

awk 'BEGIN { print "[" } { print $0"," }' $output_dir/timeline.log > tmp && mv tmp $output_dir/timeline.log
# Remove last comma, make valid JSON array
sed -i '$ s/.$/\n]/' $output_dir/timeline.log

# Extract just the eval accuracies
grep -a "eval_accuracy" $output_dir/u.log > $output_dir/evals.log
# Remove useless fields
awk -F ', ' 'BEGIN {OFS= ", "; ORS="\n"} {print $1,$2,$3,$4,$7}' $output_dir/evals.log > tmp && mv tmp $output_dir/evals.log
sed -i 's/}}/}/' $output_dir/evals.log

# Convert to valid JSON array
awk 'BEGIN { print "[" } { print $0"," }' $output_dir/evals.log > tmp && mv tmp $output_dir/evals.log
sed -i '$ s/.$/\n]/' $output_dir/evals.log

# Extract all other info
grep -E -v "init_start|init_stop|run_start|run_stop|block_start|block_stop|epoch_start|epoch_stop|eval_start|eval_accuracy|eval_stop" $output_dir/u.log > $output_dir/other_info.log
awk 'BEGIN { print "[" } { print $0"," }' $output_dir/other_info.log > tmp && mv tmp $output_dir/other_info.log
sed -i '$ s/.$/\n]/' $output_dir/other_info.log

