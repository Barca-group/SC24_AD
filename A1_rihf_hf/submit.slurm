#!/bin/bash
#SBATCH -A PROJ_g

#SBATCH -o rhf_and_rihf.out
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -N 1
#SBATCH --ntasks=2
#SBATCH --gpus-per-node=1

#SBATCH --time=00:10:00
module load hdf5

srun ./exess rihf.json
srun ./exess rhf.json
