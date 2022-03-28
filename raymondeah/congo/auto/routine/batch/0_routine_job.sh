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
python3 mine_detection.py 29.5 29.769500374003208 3.5 3.2304887442781713 0
