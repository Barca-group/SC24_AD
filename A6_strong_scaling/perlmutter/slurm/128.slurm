#!/bin/bash
#SBATCH -A PROJ_g

#SBATCH -o paracetamol_3step_n128.out
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -N 128
#SBATCH --ntasks=1152
#SBATCH --ntasks-per-node=9
#SBATCH --gpus-per-node=4

#SBATCH --time=02:00:00
module load hdf5

srun ./exess 80_paracetamol.json
