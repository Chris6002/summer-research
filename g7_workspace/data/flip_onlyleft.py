import csv
import os
from PIL import Image
dir_path = os.path.dirname(os.path.realpath(__file__))
old_path=os.path.join(dir_path,'dataset/command/0/all_three.csv')

new_path=os.path.join('dataset/command/0/test_left.csv')
# old_path=os.path.join(dir_path,'0_command.csv')
# new_path=os.path.join('test_left.csv')
print(dir_path)

with open(old_path) as in_file, open(new_path,'w') as out_file:
    csv_reader = csv.DictReader(in_file)
    new_header = csv_reader.fieldnames
    csv_writer = csv.DictWriter(out_file, new_header)
    csv_writer.writeheader()

    for index,row in enumerate(csv_reader):
        if 'right' not in row['name']:
            csv_writer.writerow(row)
            new_row=row.copy()
            new_row['name']=row['name']+'filp'
            new_row['steering'] = str(2*1476-int(row['steering']))
            csv_writer.writerow(new_row)