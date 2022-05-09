import os
import sys

def add(num1, num2):
    sum = num1 + num2

    save_path = os.getcwd()
    file_name = 'sum'
    complete_path = save_path + '/output/' + file_name + '.txt'

    file = open(complete_path, 'w')
    text = str(num1) + ' + ' + str(num2) + ' = ' + str(sum) + '\n'
    file.write(text)
    file.close()

if __name__ == '__main__':
    add(int(sys.argv[1]), int(sys.argv[2]))
