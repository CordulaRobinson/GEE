import os
import glob
        
# remove all slurm files with no exceptions
os.system("find | grep -l -L -E exception output/slurm* | xargs rm -f")

# create a txt file containing job numbers of all failed jobs
# os.system("grep JOB output/slurm* > failed.txt")
# with open('failed.txt') as file:
#     for line in file:
#         # get the index of the job number's location
#         i = line.index('JOB')
#         # get the job number
#         job_number = int(line[i:].rstrip()[-1]) + 1000000
#         # resubmit the failed job
#         os.system('find batch -name routine_job_' + str(job_number) + '.sh | xargs sbatch')

os.chdir("/scratch/agarwal.rishi/gee/rishiAgarwal/Jobs/final/output") # change to your own path to the 'output' folder
extension = 'out'
filenames = [i for i in glob.glob('*.{}'.format(extension))]

os.chdir("/scratch/agarwal.rishi/gee") # change to your own path
for file in filenames:
    # get job number by indexing into the file name
    job_number = int(file[6:-4])
    # resubmit the failed job
    os.system('find batch -name routine_job_' + str(job_number) + '.sh | xargs sbatch')
