import os

# Find failed jobs
os.system("find | grep -l -L -E exception output/slurm* | xargs rm -f")

os.system("grep JOB output/slurm* > failed.txt")
with open('failed.txt') as file:
    for line in file:
        i = line.index('JOB')
        job_number = int(line[i:].rstrip()[-1]) + 1000000

        os.system('find batch -name routine_job_' + str(job_number) + '.sh | xargs sbatch')