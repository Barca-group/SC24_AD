#!/bin/bash
#SBATCH -A PROJ_g

#SBATCH -o paracetamol_3step_n256.out
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -N 256
#SBATCH --ntasks=2304
#SBATCH --ntasks-per-node=9
#SBATCH --gpus-per-node=4

#SBATCH --time=00:20:00
module load hdf5

srun ./exess 80_paracetamol.json
