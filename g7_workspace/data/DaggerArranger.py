import csv
import numpy as np
import os
import zipfile
import preprocessing


current_folder=preprocessing.current_folder(__file__)
Dagger_folder=os.path.join(current_folder,'dagger')
temp=os.path.join(Dagger_folder,'temp')
preprocessing.unzip_dataset(temp)



print('==========================')
print('Extract all frames')
print('==========================')
video_list= preprocessing.get_filelist(temp,'.avi')
for video in video_list:
    class_num=os.path.basename(video).split('_')[0]
    iter_num=os.path.basename(video).split('.')[0].split('_')[-1]
    print("{:10} size(MB): {:>8.2f}".format(os.path.basename(video), os.path.getsize(video) / 1000000),end='  ')
    preprocessing.extract_frames(video,os.path.join(Dagger_folder,f"{class_num}/video/{iter_num}"))
    print('Done!')
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
    output_file=
    print(class_num,iter_num)
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