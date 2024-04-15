#!/bin/bash
#SBATCH -A PROJ_g

#SBATCH -o paracetamol_3step_n64.out
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -N 64
#SBATCH --ntasks=576
#SBATCH --ntasks-per-node=9
#SBATCH --gpus-per-node=4

#SBATCH --time=02:00:00
source perlm_env

srun ./exess 80_paracetamol.json
