#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=00:01:00
#SBATCH --job-name=basic_gee_job
#SBATCH --partition=short
#SBATCH --mem=1GB
module load anaconda3/3.7
source activate 
source activate ee
conda activate ee
conda init bash
python3 basic_gee.py
