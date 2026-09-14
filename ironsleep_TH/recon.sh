#!/bin/bash

#
#SBATCH -c 16					# 16 cores for fast reco
#SBATCH --mem 500G				# 0.5 mm fully sampled is around 220G, need maybe double
#SBATCH --time 1440				# 10 echoes at 2 hours per echo but some nodes take 3 hours per echo
#SBATCH -o /data/u_kuegler_software/git/loraks_reconstruction/logs/ironsleep_TH/%j.out	# redirect the output
#
# Real values for (16 cores, 500G request) are 213G RAM 8.5hrs time 27G file (PDw/T1w), 121G 6.5hrs 10G (MTw)

rawdata=$1
outdir=$2

echo "rawdata: $rawdata"
echo "outdir: $outdir"

current_dir=$(dirname "$(readlink -f "$0")")
valid_dir='(.*batch_loraksreco)'

if [[ "$current_dir" =~ $valid_dir ]]; then
# checks if recon.sh is within the batch_loraksreco/ directory
    RELPATH="${BASH_REMATCH[1]}/"
else
# else does exits and does not attempt MATLAB command
    echo "Failed to find loraksConfig.json, ensure recon.sh is within the batch_loraksreco/ directory" >&2
    exit 1
fi


# Use adjRank config if rawdata filename contains "smap" or "sens"
if [[ "$rawdata" == *"smap"* ]] || [[ "$rawdata" == *"sens"* ]]; then
    config="${RELPATH}loraksConfig_adjRank.json"
    echo "Detected 'smap' or 'sens' in filename, using adjRank config"
else
    config="${RELPATH}loraksConfig.json"
fi

start=$(date +%s)

MATLAB -v 24.2 matlab -batch "reconstruction('$rawdata','$outdir','$config');exit" -sd /data/u_kuegler_software/git/image-reconstruction

end=$(date +%s)
duration=$((end - start))
echo "Duration: $((duration / 60)) minutes"
