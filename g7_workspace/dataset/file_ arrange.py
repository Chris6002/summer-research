import os

current_folder = os.path.dirname(os.path.realpath(__file__))
video_path = current_folder + '/video'
command_path = current_folder + '/command'
temp_path = current_folder + '/temp'


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
                allFiles = subFiles + allFiles  #合并当前目录与子目录的所有文件路径
            else:
                allFiles.append(f)
        return allFiles
    else:
        return 'Error,not a dir'


saved_file = read_dir(video_path)
index_start = max(
    map(int, [name.split('/')[-1].split('_')[0]
              for name in saved_file])) + 1 if saved_file else 1

temp_file = read_dir(temp_path)

dir_name = {'Left': [], 'Right': [], 'Centre': []}

dir_name['Centre'] = [
    file_path for file_path in temp_file if 'Centre' in file_path
]

for index, name in enumerate(dir_name['Centre']):
    if '.avi' in name:
        name_base = '/' + str(index_start + index) + '_'
        centre_video_name = name
        left_video_name = name.replace('Centre', 'Left')
        right_video_name = name.replace('Centre', 'Right')
        command_name = name.replace('avi', 'csv')
        centre_videoname_new = video_path + name_base + 'center' + '.avi'
        left_videoname_new = video_path + name_base + 'left' + '.avi'
        right_videoname_new = video_path + name_base + 'right' + '.avi'
        commname_new = command_path + name_base + 'center' + '.csv'
        print(command_name)
        os.rename(command_name, commname_new)
        os.rename(centre_video_name, centre_videoname_new)
        os.rename(left_video_name, left_videoname_new)
        os.rename(right_video_name, right_videoname_new)
        # print(video_name, command_name)

# for camera in dir_name:
#     for index,name in enumerate(dir_name[camera]):
#         time=
#         name_new=str(index_start+index)+camera+