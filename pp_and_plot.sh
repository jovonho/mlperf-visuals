#!/bin/bash

# Determine which python command to use depending on platform 
unameOut="$(uname -s)"
case "${unameOut}" in
    MINGW*)     py=py;;
    *)          py=python3;;
esac

if [ $# -ne 2 ]
then
    echo "Usage: $0 <preprocessed data dir> <num gpus used>" 
done

datadir=$1
num_gpus=$2
expname=$(basename $1)

./data/preprocess_traces.sh $datadir $num_gpus
${py} timeline.py $datadir $expname