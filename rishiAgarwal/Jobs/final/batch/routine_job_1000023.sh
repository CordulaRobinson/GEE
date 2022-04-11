#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --job-name=routine_job
#SBATCH --partition=short
#SBATCH --mem=16GB
#SBATCH --output=output/slurm-1000023.out
module load anaconda3/3.7
source activate 
source activate ee
conda activate ee
conda init bash
python3 step3_mine_detection.py -113.00314459266312 -112.91331113466205 34.88081647081126 34.790929763606236 23
