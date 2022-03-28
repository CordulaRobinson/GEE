#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --job-name=ADD_5_8
#SBATCH --partition=short
#SBATCH --mem=12GB
module load anaconda3/3.7
source activate 
source activate ee
conda activate ee
conda init bash
python3 add_two_numbers.py 8 1
