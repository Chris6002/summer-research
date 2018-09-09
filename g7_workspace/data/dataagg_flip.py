import csv
import os
from PIL import Image
import numpy as np
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--classnum',  type=str)
args = parser.parse_args()
oldpath=f"dataset/command/{args.classnum}/all_three.csv"
newpath=f"dataset/command/{args.classnum}/test.csv"

dir_path = os.path.dirname(os.path.realpath(__file__))
old_path=os.path.join(dir_path,oldpath)
new_path=os.path.join(dir_path,newpath)
print(dir_path)
change_image=1
with open(old_path) as in_file, open(new_path,'w') as out_file:
    csv_reader = csv.DictReader(in_file)
    new_header = csv_reader.fieldnames
    csv_writer = csv.DictWriter(out_file, new_header)
    csv_writer.writeheader()

    for index,row in enumerate(csv_reader):
        csv_writer.writerow(row)
        new_row=row.copy()
        new_row['name']=row['name']+'filp'
        center= np.random.normal(1480,5,1)[0]
        new_row['steering'] = str(int(2*center-int(row['steering'])))
        csv_writer.writerow(new_row)


frames_folder=os.path.join(dir_path,f'dataset/video/{args.classnum}')
frames_list=[os.path.join(frames_folder,name) for name in os.listdir(frames_folder) if '.jpg' in name]

if change_image:
    for index,path in enumerate(frames_list):
        camera=os.path.basename(path).split('_')[1]
        print(index,"   ",camera)
        camerafilp=camera+'filp'
        new_path=path.replace(camera,camerafilp)
        # print(new_path)
        frame = Image.open(path)
        frame = frame.transpose(Image.FLIP_LEFT_RIGHT)
        frame.save(new_path)
