import os

# remove all slurm files with no exceptions
os.system("find | grep -l -L -E exception output/slurm* | xargs rm -f")

# create a txt file containing job numbers of all failed jobs
os.system("grep JOB output/slurm* > failed.txt")
with open('failed.txt') as file:
    for line in file:
        # get the index of the job number's location
        i = line.index('JOB')
        # get the job number
        job_number = int(line[i:].rstrip()[-1]) + 1000000
        # resubmit the failed job
        os.system('find batch -name routine_job_' + str(job_number) + '.sh | xargs sbatch')