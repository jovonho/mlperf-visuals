#!/bin/bash


grep -aE "sda\s+1" bio_python.out > writes/bio_writes/all_bio_writes

grep -aE " W " vfs_rw_time_aligned.out > writes/vfs_writes/all_vfs_writes

# Extract and count all vfs written files
awk -F ' ' '{print $8}' writes/vfs_writes/all_vfs_writes | sort | uniq -c | sort -r > tmp && mv tmp writes/vfs_writes/all_written_files


# Extract BIO and VFS writes for each PID
while read pid; do
    # Remove whitespaces and newlines from pid
    pid=${pid//[$'\t\r\n']}
    echo "Processing $pid"

    grep -a " $pid " bio_python.out | grep -aE "sda\s+1" > "writes/bio_writes/bio_writes_$pid"

    # VFS Writes
    grep -a " $pid " vfs_rw_time_aligned.out | grep -aE " W " > "writes/vfs_writes/vfs_writes_$pid"

    awk -F ' ' '{print $8}' "writes/vfs_writes/vfs_writes_$pid" | sort | uniq -c | sort -r > "writes/vfs_writes/written_files_$pid"

done < ./unique_pids



