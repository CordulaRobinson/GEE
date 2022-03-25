from wsgiref.simple_server import WSGIRequestHandler
import numpy as np
import os
import itertools
import sys

def checkstatus(string):
    status = None
    with open('/scratch/agarwal.rishi/gee/rishiAgarwal/Jobs/test_folder/sum.txt', 'r') as f:
        status = f.read()
    return status == string

# let's start from the bottom left 
i = 0
while i < 34:
    last_place_number_1 = None
    last_place_number_2 = None
    last_place_sum = None
    with open('/scratch/agarwal.rishi/gee/rishiAgarwal/Jobs/test_folder/sum.txt', 'r') as f:
        last_place_number_1 = int(f.readline()[:1])
        last_place_number_2 = int(f.readline()[:1])
        last_place_sum = int(f.readline()[:1])
    sys.stdout.write(str(i))
    bash_filename = 'test_sum_'+str(last_place_number_1)+'+'+str(last_place_number_2)+'.sh'
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
        f.write('#SBATCH --job-name=ADD_'+str(last_place_number_1)+'_'+str(last_place_number_2)+'\n')
        f.write('#SBATCH --partition=short'+'\n')
        f.write('#SBATCH --mem=12GB'+'\n')
        f.write('module load anaconda3/3.7'+'\n')
        f.write('source activate '+'\n')
        f.write('source activate ee'+'\n')
        f.write('conda activate ee'+'\n')
        f.write('conda init bash'+'\n')
        f.write('python3 '+ 'add_two_numbers.py '+ str(last_place_number_2) + ' ' + str(last_place_sum) + '\n')
    os.system('sbatch ' + bash_filename )
    while checkstatus(str(last_place_number_1) + '\n' + str(last_place_number_2) + '\n' + str(last_place_sum)):
        with open('/scratch/agarwal.rishi/gee/rishiAgarwal/Jobs/test_folder/sum.txt', 'r') as f:
            i = int(f.readlines()[2:][0])
    
    with open('/scratch/agarwal.rishi/gee/rishiAgarwal/Jobs/test_folder/done.txt', 'w') as f:
        f.write(str(i))


