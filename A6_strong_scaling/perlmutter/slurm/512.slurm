#!/bin/bash
#SBATCH -A PROJ_g

#SBATCH -o paracetamol_3step_n512.out
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -N 512
#SBATCH --ntasks=4608
#SBATCH --ntasks-per-node=9
#SBATCH --gpus-per-node=4

#SBATCH --time=01:00:00
module load hdf5

srun ./exess 80_paracetamol_n512.json
