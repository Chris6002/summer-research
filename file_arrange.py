import os

current_folder = os.path.dirname(os.path.realpath(__file__))
video_path = current_folder + '/video'
command_path = current_folder + '/command'
temp_path = current_folder + '/temp'






# unzip files

import zipfile

for i in range(2):
    zipfiles = [zipf for zipf in os.listdir(temp_path) if 'zip' in zipf]
    if len(zipfiles)>0:
        for name in zipfiles:
            file_path = temp_path+'/'+name
            f = zipfile.ZipFile(file_path)
            print('extracing:  '+name)
            f.extractall(temp_path)
            f.close()
            os.remove(file_path)
        print('Unzip all zips')
    else:
        print("No zip files")




def read_dir(dirPath):
    if dirPath[-1] == '/':
        print('文件夹路径末尾不能加/')
        return
    allFiles = []
    if os.path.isdir(dirPath):
        fileList = os.listdir(dirPath)
        for f in fileList:
            f = dirPath + '/' + f
            if os.path.isdir(f):
                subFiles = read_dir(f)
                allFiles = subFiles + allFiles  # 合并当前目录与子目录的所有文件路径
            else:
                allFiles.append(f)
        return allFiles
    else:
        return 'Error,not a dir'


# get start index


saved_file = read_dir(video_path)
index_start = max(
    map(int, [name.split('/')[-1].split('_')[0]
              for name in saved_file])) + 1 if saved_file else 1
print("Already have "+str(index_start-1)+" videos")
temp_file = read_dir(temp_path)

dir_name = {'Left': [], 'Right': [], 'Centre': []}

dir_name['Centre'] = [
    file_path for file_path in temp_file if 'Centre' in file_path
]
for a in dir_name['Centre']:
    print(a)


# move files
for index, name in enumerate(dir_name['Centre']):
    if '.avi' in name:
        name_base = '/' + str(index_start + index) + '_'
        centre_video_name = name
        left_video_name = name.replace('Centre', 'Left')
        right_video_name = name.replace('Centre', 'Right')
        command_name = name.replace('Centre', 'Command')
        command_name = command_name.replace('.avi', '_command.csv')
        centre_videoname_new = video_path + name_base + 'center' + '.avi'
        left_videoname_new = video_path + name_base + 'left' + '.avi'
        right_videoname_new = video_path + name_base + 'right' + '.avi'
        commname_new = command_path + name_base + 'center' + '.csv'
        os.rename(command_name, commname_new)
        os.rename(centre_video_name, centre_videoname_new)
        os.rename(left_video_name, left_videoname_new)
        os.rename(right_video_name, right_videoname_new)
print("Cleaning up......")
import shutil
shutil.rmtree(temp_path)
os.mkdir(temp_path)
