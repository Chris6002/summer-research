import csv
import os
from PIL import Image
dir_path = os.path.dirname(os.path.realpath(__file__))
old_path=os.path.join(dir_path,'dataset/command/0/all_three.csv')
new_path=os.path.join('dataset/command/0/test.csv')
print(dir_path)

with open(old_path) as in_file, open(new_path,'w') as out_file:
    csv_reader = csv.DictReader(in_file)
    new_header = csv_reader.fieldnames
    csv_writer = csv.DictWriter(out_file, new_header)
    csv_writer.writeheader()

    for index,row in enumerate(csv_reader):
        csv_writer.writerow(row)
        new_row=row.copy()
        new_row['name']=row['name']+'filp'
        new_row['steering'] = str(2*1476-int(row['steering']))
        csv_writer.writerow(new_row)


frames_folder=os.path.join(dir_path,'dataset/video/0')
frames_list=[os.path.join(frames_folder,name) for name in os.listdir(frames_folder) if '.jpg' in name]

for index,path in enumerate(frames_list[:10]):
    camera=os.path.basename(path).split('_')[1]
    camerafilp=camera+'filp'
    new_path=path.replace(camera,camerafilp)
    # print(new_path)
    frame = Image.open(path)
    frame = frame.transpose(Image.FLIP_LEFT_RIGHT)
    frame.save(new_path)
