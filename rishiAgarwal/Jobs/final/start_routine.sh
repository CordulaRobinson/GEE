#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --job-name=start_routine
#SBATCH --partition=short
#SBATCH --mem=1GB
module load anaconda3/3.7
source activate 
source activate ee
conda activate ee
conda init bash
python3 step2_multiple_jobs.py -115.06931412668766 35.379488360140314 -115.84385025950016 34.88081647081126
