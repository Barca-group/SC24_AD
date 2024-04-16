#!/bin/bash
#SBATCH -A m4265_g

#SBATCH -o 80_paracetamol_large_scale.out
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -N 1536
#SBATCH --ntasks=13824
#SBATCH --ntasks-per-node=9
#SBATCH --gpus-per-node=4

#SBATCH --time=00:30:00
source perlm_env
export OMP_NUM_THREADS=40
srun ./exess large_scale_paracetamol.json
