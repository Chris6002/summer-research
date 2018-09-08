import csv
import numpy as np
import os
import zipfile
import preprocessing
from PIL import Image

current_folder=preprocessing.current_folder(__file__)
Dagger_folder=os.path.join(current_folder,'dagger')
temp=os.path.join(Dagger_folder,'temp')

print('==========================')
print('Unzip dataset')
print('==========================')
preprocessing.unzip_dataset(temp)

useful_frame=[]

print('==========================')
print('Extract all frames')
print('==========================')
video_list= preprocessing.get_filelist(temp,'.avi')
for video in video_list:
    class_num=os.path.basename(video).split('_')[0]
    iter_num=os.path.basename(video).split('.')[0].split('_')[-1]
    print("{:10} size(MB): {:>8.2f}".format(os.path.basename(video), os.path.getsize(video) / 1000000))
    preprocessing.extract_frames(video,os.path.join(Dagger_folder,f"{class_num}/video/{iter_num}"))
print('==========================')
print('Decay command')
print('==========================')
def decay(diff,len,index,options):
    if options=='ex':
        sign=-1 if diff<0 else 1
        w=np.log(abs(int(diff)))/len
        return sign*np.exp(w*(index+1))
    elif options=='sigmoid':
        sign = -1 if diff < 0 else 1
        w=np.exp(abs(int(diff)))/len
        return np.log(w*(index+1))*sign
    elif options=='linear':
        sign = -1 if diff < 0 else 1
        w=abs(int(diff))/len
        return w*(index+1)*sign
command_list=preprocessing.get_filelist(temp,'.csv')
for command_file in command_list:
    class_num=os.path.basename(command_file).split('_')[0]
    iter_num=os.path.basename(command_file).split('.')[0].split('_')[-2]
    output_file=os.path.join(Dagger_folder,f'{class_num}/command/{iter_num}.csv')
    input_file=command_file
    with open(input_file) as csv_file, open(output_file, 'w') as out_file:
        csv_reader = csv.DictReader(csv_file)
        csv_writer = csv.DictWriter(out_file, csv_reader.fieldnames)
        csv_writer.writeheader()
        command_queue = []
        for row in csv_reader:
            # print(row)
            command_queue.append(row)
            # for i in command_queue:
            #     print(i)
            if len(command_queue) > 40:

                adjust_list = [int(command['stage']) for command in command_queue]
                adjust = command_queue[-1]["stage"]
                adjust_pre = command_queue[-2]["stage"]
                if adjust_pre == '0' and adjust == '1' and sum(adjust_list)<5:
                    change_number = command_queue[-1]["frame"]
                    diff = int(command_queue[-1]["steering"]) - int(command_queue[-2]["steering"])
                    for index, command in enumerate(command_queue[:-1]):
                        # print(command['steering'])
                        command['useful'] = 1
                        command['steering'] = str(int(command['steering']) + int(
                            decay(diff, len(command_queue), index + 1, options='linear')))
                saving = command_queue.pop(0)
                if saving['useful']==1:
                    if abs(int(saving['steering'])-1480)>80:
                        useful_frame.append(int(saving['frame']))
                        csv_writer.writerow(saving)
                        new_saving=saving.copy()
                        new_saving['name']=new_saving['name']+'_flip'
                        new_saving['steering']=str(2*1480-int(new_saving['steering']))
                        csv_writer.writerow(new_saving)
        if len(command_queue)>0:
            csv_writer.writerow(saving)
    print(output_file)
print('==========================')
print('Filp Image')
print('==========================')
print('useful frame: ',len(useful_frame))
class_folderlist=preprocessing.get_folderlist(Dagger_folder,'temp')
index=0
for class_folder in class_folderlist:
    frame_folder=os.path.join(class_folder,'video')
    frame_list=preprocessing.get_filelist(frame_folder,'jpg')
    for frame in frame_list:
        frame_num=int(os.path.basename(frame).split('.')[0].split('_')[-1])
        iternum=os.path.basename(frame).split('_')[0]
        framename=os.path.basename(frame).split('_')[-1]

        if frame_num in useful_frame and 'flip' not in frame:
            index+=1
            # print(index)
            iterflip=iternum+'_flip_'
            newframe=os.path.join(os.path.dirname(frame),iterflip+framename)
            image=Image.open(frame)
            image=image.transpose(Image.FLIP_LEFT_RIGHT)
            image.save(newframe)
print('flip number: ',index)
    # frame_list=preprocessing()

# inputcsv='0_command.csv'
# outputcsv='test_decay.csv'
# def decay(diff,len,index,options):
#     if options=='ex':
#         sign=-1 if diff<0 else 1
#         w=np.log(abs(int(diff)))/len
#         return sign*np.exp(w*(index+1))
#     elif options=='sigmoid':
#         sign = -1 if diff < 0 else 1
#         w=np.exp(abs(int(diff)))/len
#         return np.log(w*(index+1))*sign
#     elif options=='linear':
#         sign = -1 if diff < 0 else 1
#         w=abs(int(diff))/len
#         return w*(index+1)*sign
#
# with open(inputcsv) as csv_file, open(outputcsv, 'w') as out_file:
#     csv_reader = csv.DictReader(csv_file)
#     csv_writer = csv.DictWriter(out_file, csv_reader.fieldnames)
#     csv_writer.writeheader()
#     command_queue=[]
#     for row in csv_reader:
#         # print(row)
#         command_queue.append(row)
#         # for i in command_queue:
#         #     print(i)
#         if len(command_queue)>40:
#             adjust=command_queue[-1]["stage"]
#             adjust_pre=command_queue[-2]["stage"]
#             if adjust_pre=='0' and adjust=='1':
#                 change_number=command_queue[-1]["frame"]
#                 diff=int(command_queue[-1]["steering"])-int(command_queue[-2]["steering"])
#                 for index,command in enumerate(command_queue[:-1]):
#                     print(command['steering'])
#                     command['useful']=1
#                     command['steering']=str(int(command['steering'])+int(decay(diff,len(command_queue),index+1,options='linear')))
#
#             #   for i in command_queue:
#             #     every i decay by little
#             saving = command_queue.pop(0)
#             csv_writer.writerow(saving)

# TODO: 1.change command file
# TODO: 2.extract file and remove non-usefull frame