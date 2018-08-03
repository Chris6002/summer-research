import csv


dataset = [{'steering': 1000, 'speed': 2000, 'category': 0}, {'steering': 1000, 'speed': 2000, 'category': 0},
           {'steering': 1000, 'speed': 2000, 'category': 0}, {'steering': 1000, 'speed': 2000, 'category': 0}, 
           {'steering': 1000, 'speed': 2000, 'category': 0}]

## write
f = open('names.csv', 'w')
fnames = ['steering', 'speed', 'category']
writer = csv.DictWriter(f, fieldnames=fnames)
writer.writeheader()
for data in dataset:

    # print(data)
    writer.writerow(data)

f.close()

## read
with open('names.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['steering'], row['speed'], row['category'])
