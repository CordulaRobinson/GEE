import csv
import sys

def func(arg1, arg2):
	header = ['name', 'area', 'country_code2', 'arg1', 'arg2']
	data = ['India', 652090, 'IN', arg1, arg2]

	with open('/scratch/agarwal.rishi/countries.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow(header)
		writer.writerow(data)

if __name__ == '__main__':
	func(int(sys.argv[1]), int(sys.argv[2]))
