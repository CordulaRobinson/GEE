#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --job-name=routine_job
#SBATCH --partition=short
#SBATCH --mem=16GB
#SBATCH --output=output/slurm-1000140.out
module load anaconda3/3.7
source activate 
source activate ee
conda activate ee
conda init bash