import os
import csv

current_folder=os.path.dirname(os.path.realpath(__file__))
inputfile=os.path.join(current_folder,'1.csv')

outputpath=os.path.join(current_folder,'test.csv')
with open(outputpath) as out_file:
    
    field=csv.DictReader(out_file).fieldnames
with open(inputfile) as csv_file, open(outputpath,'a') as out_file:
    reader=csv.DictReader(csv_file)
    
    writer=csv.DictWriter(out_file,field)
   
   
    for row in reader:
        newrow=row.copy()
        newrow.pop('stage')
        newrow.pop('useful')
        writer.writerow(newrow)