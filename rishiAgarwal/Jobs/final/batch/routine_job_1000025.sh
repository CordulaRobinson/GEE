#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --job-name=routine_job
#SBATCH --partition=short
#SBATCH --mem=16GB
#SBATCH --output=output/slurm-1000025.out
module load anaconda3/3.7
source activate 
source activate ee
conda activate ee
conda init bash
python3 step3_mine_detection.py -112.82347767666099 -112.73364421865992 34.88081647081126 34.790929932879784 25