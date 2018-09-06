import csv
import os
import numpy as np
dir_path = os.path.dirname(os.path.realpath(__file__))
old_path=os.path.join(dir_path,'dataset/command/0/all_three.csv')
import matplotlib.pyplot as plt
steer=[]
with open(old_path) as in_file:
    csv_reader = csv.DictReader(in_file)

    for index, row in enumerate(csv_reader):
        if 'center' in row['name']:
            steer.append(int(row['steering']))
print(sum(steer)/len(steer))

counts, bins, bars=plt.hist(steer,bins=1000)
print(bins[np.argmax(counts)])
plt.show()