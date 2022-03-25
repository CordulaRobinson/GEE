#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=1:00:00
#SBATCH --job-name=Submit_Jobs_Test
#SBATCH --partition=short

module load anaconda3/3.7
source activate
source activate ee
conda activate ee
conda init bash
python3 submit_jobs_test.py
