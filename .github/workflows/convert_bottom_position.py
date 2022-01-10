import csv
import sys
import os

if len(sys.argv) != 3:
  print('Invalid Number of arguments')
  quit()

script_dir = os.path.dirname(__file__)
abs_file_path_input = os.path.join(script_dir, sys.argv[1])
abs_file_path_output = os.path.join(script_dir, sys.argv[2])

input_file = open(abs_file_path_input)
output_file = open(abs_file_path_output, 'w')

startwriter = csv.writer(output_file)

csv_f = csv.reader(input_file)


for row in csv_f:
  print(row)
  if row[6] == 'bottom':
    row[5] = float(row[5])+180.0
    if row[5] >= 360.0:
      row[5] -= 360.0
  startwriter.writerow(row)
  print(row)

