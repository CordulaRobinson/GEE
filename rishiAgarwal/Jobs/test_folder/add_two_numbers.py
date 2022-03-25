import os
import sys

def add(num1, num2):
    sum = num1 + num2

    with open('/scratch/agarwal.rishi/gee/rishiAgarwal/Jobs/test_folder/sum.txt', 'w') as f:
        f.truncate(0)
        f.write(str(num1) + '\n')
        f.write(str(num2) + '\n')
        f.write(str(sum))
        
if __name__ == '__main__':
    add(int(sys.argv[1]), int(sys.argv[2]))
