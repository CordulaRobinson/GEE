#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --job-name=routine_job
#SBATCH --partition=short
#SBATCH --mem=16GB
module load anaconda3/3.7
source activate 
source activate ee
conda activate ee
conda init bash
python3 mine_detection.py 26 26.44916729000535 -2.6951066992522574 -3.1442880771376007 42
