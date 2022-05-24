#!/bin/bash

mkdir -p open_data/stats

for f in $(find open_data/ –maxdepth 1 –type f)
do
    awk -F ' ' '{print $5}' "open_data/$f" | grep case_ | sort | uniq -c | sort -r > "open_data/stats/file_counts_$f"
done
