import os
import csv

os.system("cat results/*csv > results/compiled.csv") # compile all results into one csv file
os.system("rm -rf results/job*") # remove individual results files
os.system("rm -rf output/slurm*") # remove slurm files
os.system("rm -rf slurm*") # remove slurm files
os.system("rm -rf batch/routine*") # remove batch files
os.system("rm queue.txt") # remove temp queue file
os.system("rm failed.txt") # remove failed jobs txt file
os.system("rm start_routine.sh") # remove step 1 bash file
os.system("python3 add_scores.py compiled") # call next step with desired csv file name (do not include .csv)
