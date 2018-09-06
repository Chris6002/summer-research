import csv
import os
from PIL import Image
import argparse
parser = argparse.ArgumentParser()

args = parser.parse_args()
dir_path = os.path.dirname(os.path.realpath(__file__))
old_path=os.path.join(dir_path,"dataset/command/0/all_three.csv")
new_path=os.path.join(dir_path,"dataset/command/0/leftonly.csv")
print(dir_path)

with open(old_path) as in_file, open(new_path,'w') as out_file:
    csv_reader = csv.DictReader(in_file)
    new_header = csv_reader.fieldnames
    csv_writer = csv.DictWriter(out_file, new_header)
    csv_writer.writeheader()

    for index,row in enumerate(csv_reader):
        if 'right' not in row['name']:
            csv_writer.writerow(row)
