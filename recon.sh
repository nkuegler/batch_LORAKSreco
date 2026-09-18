#!/bin/bash

#
#SBATCH -c 16					# 16 cores for fast reco
#SBATCH --mem 500G				# 0.5 mm fully sampled is around 220G, need maybe double
#SBATCH --time 1440				# 10 echoes at 2 hours per echo but some nodes take 3 hours per echo
#SBATCH -o /data/u_kuegler_software/git/batch_LORAKSreco/logs/ironsleep_TH/%j.out	# redirect the output
#
# Real values for (16 cores, 500G request) are 213G RAM 8.5hrs time 27G file (PDw/T1w), 121G 6.5hrs 10G (MTw)

rawdata=$1
outdir=$2
script_dir=$3

echo "rawdata: $rawdata"
echo "outdir: $outdir"
echo "script_dir: $script_dir"

# recon_call.py, recon.sh, and loraksConfig json need to be in the same directory!

# Use adjRank config if rawdata filename contains "smap" or "sens"
if [[ "$rawdata" == *"smap"* ]] || [[ "$rawdata" == *"sens"* ]]; then
    config="${script_dir}/loraksConfig_adjRank.json"
    echo "Detected 'smap' or 'sens' in filename, using adjRank config"
else
    config="${script_dir}/loraksConfig.json"
fi

if ! [ -f "${config}" ]; then
    echo "Error: Failed to find config: ${config}"
    exit 1
fi

start=$(date +%s)

MATLAB -v 24.2 matlab -batch "reconstruction('$rawdata','$outdir','$config');exit" -sd /data/u_kuegler_software/git/image-reconstruction
matlab_status=$?

end=$(date +%s)
duration=$((end - start))
echo "Duration: $((duration / 60)) minutes"

exit "$matlab_status"
