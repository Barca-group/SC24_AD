#!/bin/bash 


module load gcc
module load rocm/5.4.3
module load hdf5
module load magma
module load cmake
export HDF5_USE_FILE_LOCKING=FALSE

srun -N 1 --ntasks=2 --gpus-per-node=1 -c 2 ./exess  paracetamol_no_rtat.json
srun -N 1 --ntasks=2 --gpus-per-node=1 -c 2 ./exess  paracetamol_wrtat.json 
srun -N 1 --ntasks=2 --gpus-per-node=1 -c 2 ./exess  urea_no_rtat.json 
srun -N 1 --ntasks=2 --gpus-per-node=1 -c 2 ./exess  urea_wrtat.json
