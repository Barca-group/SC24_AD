#!/bin/bash
#SBATCH -A PROJX
#SBATCH -J 4096_weak
#SBATCH -e joberr.%j
#SBATCH -o jobout.%j
#SBATCH -t 0:30:00
#SBATCH -p batch
#SBATCH -N 4096


module load rocm/5.4.3
module load magma
module load hdf5
export HDF5_USE_FILE_LOCKING="FALSE"
export OMP_NUM_THREADS=2
export MPICH_ENV_DISPLAY=1
export MPICH_VERSION_DISPLAY=1
export MPICH_ABORT_ON_ERROR=1
export FI_CXI_RX_MATCH_MODE="hybrid"


input="inputs/urea_91frag.json"
nnodes=$SLURM_JOB_NUM_NODES
nteamspernode=8
ngpusperteam=1
taskspernode=$((1 + nteamspernode * (ngpusperteam + 1)))
ranks=$((nnodes * taskspernode))
ngpuspernode=8
current_time=$(date "+%Y-%m-%d_%H-%M-%S")
output="$input"_"$current_time"_"nnodes:$nnodes"_"ranks:$ranks"_"ngpus:$ngpuspernode.out"

FI_MR_CACHE_MONITOR=kdreg2 srun -N $nnodes --ntasks=$ranks --ntasks-per-node=$taskspernode -c 2 --gpus-per-node=$ngpuspernode ./exess $input >& $output

