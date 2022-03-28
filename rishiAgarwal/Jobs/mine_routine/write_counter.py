import os
import sys

iter1 = sys.argv[1]
iter2 = sys.argv[2]

cwd = os.getcwd()
iter_file = os.path.join(cwd,'iterfile.txt')

with open(iter_file, 'w') as f:
     f.write(str(int(iter1))+','+str(int(iter2))+'\n')


