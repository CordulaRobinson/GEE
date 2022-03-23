#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=1:00:00
#SBATCH --job-name=Routine_Squares_CSV_Export
#SBATCH --partition=short

module load anaconda3/3.7
source activate
source activate ee
conda activate ee
conda init bash
python3 Routine_Square_Code.py [[27.350233348102517,-7.57841301205225],  [27.436407359332986,-7.57841301205225], [27.436407359332986,-7.518171474050515], [27.350233348102517,-7.518171474050515]] 0.5 









