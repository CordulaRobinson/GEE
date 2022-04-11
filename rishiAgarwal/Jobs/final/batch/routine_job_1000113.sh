#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --job-name=routine_job
#SBATCH --partition=short
#SBATCH --mem=16GB
#SBATCH --output=output/slurm-1000113.out
module load anaconda3/3.7
source activate 
source activate ee
conda activate ee
conda init bash
python3 step3_mine_detection.py -104.9181333725671 -104.82829991456603 34.88081647081126 34.790937113773055 113