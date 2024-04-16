#!/bin/bash 


srun -N 1 --ntasks=2 --gpus-per-node=1 -c 2 ./exess  no_rtat.json
srun -N 1 --ntasks=2 --gpus-per-node=1 -c 2 ./exess  rtat.json 
