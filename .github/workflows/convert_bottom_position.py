import csv
import sys

if len(sys.argv) != 3:
  print('Invalid Number of arguments')
  quit()

input_file = open(sys.argv[1])
output_file = open(sys.argv[2], 'w')

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

