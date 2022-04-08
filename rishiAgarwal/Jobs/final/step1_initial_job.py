import os
import sys

# Write the bash file, named 'start_routine.sh'
bash_filename = 'start_routine.sh'
with open(bash_filename,'w') as f:
    # one node, one hour
    # name of job is start_routine
    # short partition, 1 GB memory
    # load up conda
    # execute 'step2_multiple_jobs.py' to divide given area into multiple jobs
    # the arguments passed are the bounding box - corner coordinates entered when this file is called
    ## lon min, lon max, lat max, lat min
    f.write('#!/bin/bash'+'\n')
    f.write('#SBATCH --nodes=1'+'\n')
    f.write('#SBATCH --time=01:00:00'+'\n')
    f.write('#SBATCH --job-name=start_routine'+'\n')
    f.write('#SBATCH --partition=short'+'\n')
    f.write('#SBATCH --mem=1GB'+'\n')
    f.write('module load anaconda3/3.7'+'\n')
    f.write('source activate '+'\n')
    f.write('source activate ee'+'\n') # change to your own anaconda environment
    f.write('conda activate ee'+'\n') # change to your own anaconda environment
    f.write('conda init bash'+'\n')
    f.write('python3 step2_multiple_jobs.py ' + sys.argv[1] + ' ' + sys.argv[2] + ' ' + sys.argv[3] + ' ' + sys.argv[4] + '\n')

# Now we will submit the job (the bash_filename) written above
os.system("sbatch "+str(bash_filename))
