#!/bin/bash
#SBATCH -A m4265_g

#SBATCH -o 6PQ5_5ps_async.out
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -N 64
#SBATCH --ntasks-per-node=9
#SBATCH --cpus-per-task=4
#SBATCH --gpus-per-node=4

#SBATCH --time=4:40:00

srun ./exess 6PQ5_5ps_async.json
