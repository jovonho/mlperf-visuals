#!/bin/bash

# Run this after the other scripts since
# this assumes folders and files exist

if [ $# -ne 1 ]
then
    echo "Usage: $0 datadir"
    exit -1
fi

datadir=$1
outdir=$1


if [[ ! -d $outdir/bio_hist ]]
then
    echo "Creating output directory $outdir/bio_hist"
    mkdir $outdir/bio_hist
fi
if [[ ! -d $outdir/open_hist ]]
then
    echo "Creating output directory $outdir/open_hist"
    mkdir $outdir/open_hist
fi
if [[ ! -d $outdir/read_hist ]]
then
    echo "Creating output directory $outdir/read_hist"
    mkdir $outdir/read_hist
fi



for f in $(ls $datadir/bio_data)
do
    awk -F ' ' '{ printf $3","$5","$6"\n"}' "$datadir/bio_data/$f" > "$outdir/bio_hist/hist_$f"
done
cat $outdir/bio_hist/hist_* > $outdir/bio_hist/combined

for f in $(ls $datadir/open_data)
do
    awk -F ' ' '{print $3}' "$datadir/open_data/$f" > "$outdir/open_hist/hist_$f"
done
cat $outdir/open_hist/hist_* > $outdir/open_hist/combined

for f in $(ls $datadir/read_data)
do
    awk -F ' ' '{printf "R,"$4","$3"\n"}' "$datadir/read_data/$f" > "$outdir/read_hist/hist_$f"
done
cat $outdir/read_hist/hist_* > $outdir/read_hist/combined


# for f in $(ls vfsrw_data)
# do
#     # BUGFIX
#     py vfsrw_bugfix.py "vfsrw_data/$f"
#     awk -F ' ' '{print $3","$4","$5","$6}' "vfsrw_data/$f" > "vfsrw_data_hist/hist_$f"
# done
# # Concat all pid files into a big one as well
# cat vfsrw_data_hist/hist_* > vfsrw_data_hist/comb