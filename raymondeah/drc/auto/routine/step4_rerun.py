import os

#os.system("grep -E exception output/slurm* > error_log.txt")
#os.system("cd output")
os.system("find | grep -l -L -E exception output/slurm* | xargs rm -f")

# failed = os.system("grep origin.py output/slurm*")
# print(failed)

os.system("grep JOB output/slurm* > failed.txt")
with open('failed.txt') as file:
    for line in file:
        i = line.index('JOB')
        #print(line[i:].rstrip()[-1])
        job_number = int(line[i:].rstrip()[-1]) + 1000000
        #print(job_number)
        #print(os.system('find batch -name routine_job_' + str(job_number) + '.sh'))

        os.system('find batch -name routine_job_' + str(job_number) + '.sh | xargs sbatch')
        #os.system('python3 ' + line[i:].rstrip())