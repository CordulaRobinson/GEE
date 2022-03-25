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
python3 mine_detection.py 27.796669160021395 28.245836450026744 -1.7967377995015048 -2.2459211917391153 32
