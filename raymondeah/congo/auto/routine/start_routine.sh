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
python3 multiple_jobs.py 29 29.5 3.5 3