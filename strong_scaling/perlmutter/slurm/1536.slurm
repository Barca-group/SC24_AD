#!/bin/bash
#SBATCH -A PROJ_g

#SBATCH -o 80paracetamol_3step_n1536.out
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -N 1536
#SBATCH --ntasks=13824
#SBATCH --ntasks-per-node=9
#SBATCH --gpus-per-node=4

#SBATCH --time=00:45:00
source perlm_env

srun ./exess 80_paracetamol.json
