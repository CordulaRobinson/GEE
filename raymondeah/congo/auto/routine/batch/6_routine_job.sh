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
python3 mine_detection.py 28.695003740032092 29.14417103003744 0 -0.4491844498753762 6
