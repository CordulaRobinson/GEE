import numpy as np
import os

last_place_number_1 = None
last_place_number_2 = None
last_place_sum = None
with open('/scratch/agarwal.rishi/gee/rishiAgarwal/Jobs/test_folder/sum.txt', 'r') as f:
    last_place_number1 = f.readline()
    last_place_number2 = f.readline()
    last_place_sum = f.readline()


# let's start from the bottom left 

for i in range(34):
    bash_filename = 'test_sum_'+str(last_place_number1)+'+'+str(last_place_number2)+'.sh'
    with open(bash_filename, 'w') as f:
        # one node, one hour
        # name of job is DCR_i_j
        # 12 GB memory
        # load up conda
        # execute 'gee_dcr.py' (your jupyter codes turned to .py)
        # the arguments passed are the bounding box (1x1 degree for now)
        # plus the high res smaple size == 0.0025 degree
        f.write('#!/bin/bash'+'\n')
        f.write('#SBATCH --nodes=1'+'\n')
        f.write('#SBATCH --time=01:00:00'+'\n')
        f.write('#SBATCH --job-name=DCR_'+str(last_place_number1)+'_'+str(last_place_number2)+'\n')
        f.write('#SBATCH --partition=short'+'\n')
        f.write('#SBATCH --mem=12GB'+'\n')
        f.write('module load anaconda3/3.7'+'\n')
        f.write('source activate '+'\n')
        f.write('source activate MyEnv'+'\n')
        f.write('conda activate MyEnv'+'\n')
        f.write('conda init bash'+'\n')
        f.write('add_two_numbers.py '+ str(last_place_number2) + ' ' + str(last_place_sum) + '\n')
    with open('sum.txt', 'r') as f:
        f.readline()
        f.readline()
        i = f.readline()


