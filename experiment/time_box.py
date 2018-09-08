import os
import csv
import numpy as np 
import matplotlib as mpl 

## agg backend is used to create plot as a .png file
# mpl.use('agg')

import matplotlib.pyplot as plt
current_folder=os.path.dirname(os.path.realpath(__file__))
file_list=[os.path.join(current_folder,f) for f in os.listdir(current_folder) if 'csv' in f]
for file in file_list:
    with open(file) as csv_file:
        csv_reader=csv.reader(csv_file)
        data=[]
        for line in csv_reader:
            data.append(float(line[1]))
plt.boxplot(data, patch_artist=True)
plt.show()

