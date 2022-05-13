#!/bin/bash

# Hardcoded to merge the 3 traces
tail -n+3 bio.out >> comb.out
tail -n+3 open.out >> comb.out
tail -n+3 vfs_rw.out >> comb.out
sort comb.out >> combined.out
rm comb.out