#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --job-name=routine_job
#SBATCH --partition=short
#SBATCH --mem=16GB
#SBATCH --output=output/slurm-%j.out
module load anaconda3/3.7
source activate 
source activate ee
conda activate ee
conda init bash
python3 step3_routine.py 29.859333832004282 29.949167290005352 3.2304884103735585 3.1406512362262875 22
