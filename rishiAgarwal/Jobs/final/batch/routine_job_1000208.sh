#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --job-name=routine_job
#SBATCH --partition=short
#SBATCH --mem=64GB
#SBATCH --output=output/slurm-%j.out
module load anaconda3/3.7
source activate 
source activate ee
conda activate ee
conda init bash
python3 step3_routine.py -96.38395486246574 -96.29412140446468 35.379488360140314 35.28961616896477 208
