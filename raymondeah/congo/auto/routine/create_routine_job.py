import os
import sys

job_num = sys.argv[5]
bash_filename = 'batch/' + str(job_num) + '_routine_job.sh'
with open(bash_filename,'w') as f:
    # one node, one hour
    # name of job is DCR_i_j
    # # 12 GB memory
    # load up conda
    # execute 'gee_dcr.py' (your jupyter codes turned to .py)
    # the arguments passed are the bounding box (1x1 degree for now)
    # plus the high res smaple size == 0.0025 degree
    f.write('#!/bin/bash'+'\n')
    f.write('#SBATCH --nodes=1'+'\n')
    f.write('#SBATCH --time=01:00:00'+'\n')
    f.write('#SBATCH --job-name=routine_job'+'\n')
    f.write('#SBATCH --partition=short'+'\n')
    f.write('#SBATCH --mem=16GB'+'\n')
    f.write('module load anaconda3/3.7'+'\n')
    f.write('source activate '+'\n')
    f.write('source activate ee'+'\n')
    f.write('conda activate ee'+'\n')
    f.write('conda init bash'+'\n')
    f.write('python3 mine_detection.py ' + sys.argv[1] + ' ' + sys.argv[2] + ' ' + sys.argv[3] + ' ' + sys.argv[4] + ' ' + job_num + '\n')

# now we will submit the job (the bash_filename) written abobe
os.system("sbatch "+str(bash_filename))
