#!/bin/bash

if [[ $# -eq 3 ]]; 
then
    out="combined.out"
else
    out=$4
fi

tail -n+3 $1 >> comb.out
tail -n+3 $2 >> comb.out
tail -n+3 $3 >> comb.out
tail -n+3 $4 >> comb.out
sort comb.out >> $5
rm comb.out