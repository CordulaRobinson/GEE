#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=1:00:00
#SBATCH --job-name=two_plus_three
#SBATCH --partition=short

module load anaconda3/3.7
source acivate
source activate ee
conda activate ee
conda init bash
python3 add_two_numbers.py 10 7
