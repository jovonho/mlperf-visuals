#!/bin/bash

# Run this after the other scripts since
# this assumes folders and files exist

if [[ ! -d ./bio_data_hist ]]
then
    echo "Creating output directory bio_data_hist"
    mkdir bio_data_hist
fi
if [[ ! -d ./open_data_hist ]]
then
    echo "Creating output directory open_data_hist"
    mkdir open_data_hist
fi
if [[ ! -d ./vfsopen_data_hist ]]
then
    echo "Creating output directory vfsopen_data_hist"
    mkdir vfsopen_data_hist
fi
if [[ ! -d ./vfsrw_data_hist ]]
then
    echo "Creating output directory vfsrw_data_hist"
    mkdir vfsrw_data_hist
fi

# # Convert 0/1 type to R/W
# for f in $(ls bio_data)
# do
#     awk -F ' ' '{ if ($3 == "0") printf "R,"; else printf "W,"; printf $5","$6"\n"}' "bio_data/$f" > "bio_data_hist/hist_$f"
# done
# cat bio_data_hist/hist_* > bio_data_hist/comb


# for f in $(ls open_data)
# do
#     awk -F ' ' '{print $4}' "open_data/$f" > "open_data_hist/hist_$f"
# done
# cat open_data_hist/hist_* > open_data_hist/comb

# for f in $(ls vfsopen_data)
# do
#     awk -F ' ' '{print $4}' "vfsopen_data/$f" > "vfsopen_data_hist/hist_$f"
# done
# cat vfsopen_data_hist/hist_* > vfsopen_data_hist/comb


for f in $(ls vfsrw_data)
do
    # BUGFIX
    py vfsrw_bugfix.py "vfsrw_data/$f"
    awk -F ' ' '{print $3","$4","$5","$6}' "vfsrw_data/$f" > "vfsrw_data_hist/hist_$f"
done
# Concat all pid files into a big one as well
cat vfsrw_data_hist/hist_* > vfsrw_data_hist/comb