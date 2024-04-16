#!/bin/bash
#SBATCH -A PROJ_g

#SBATCH -o cutoffs.out
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -N 1
#SBATCH --ntasks=9
#SBATCH --gpus-per-node=4

#SBATCH --time=00:35:00
module load hdf5

srun ./exess cutoffs.json
