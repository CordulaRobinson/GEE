#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --job-name=ten_plus_seven
#SBATCH --partition=short
#SBATCH --mem=1GB

module load anaconda3/3.7
source activate
source activate ee
conda activate ee
conda init bash
python3 add_two_numbers.py 10 7
