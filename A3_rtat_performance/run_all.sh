#!/bin/bash 


srun -N 1 --ntasks=2 --gpus-per-node=1 -c 2 ./exess  nortat_paracetamol.json
srun -N 1 --ntasks=2 --gpus-per-node=1 -c 2 ./exess  rtat_paracetamol.json 
srun -N 1 --ntasks=2 --gpus-per-node=1 -c 2 ./exess  nortat_urea.json
srun -N 1 --ntasks=2 --gpus-per-node=1 -c 2 ./exess  rtat_urea.json 
