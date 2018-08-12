import os

current_folder = os.path.dirname(os.path.realpath(__file__))
video_path = current_folder + '/video'
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
index_start = max([name.split("_")[0]
                   for name in saved_file]) + 1 if not saved_file else 1
print(index_start)

# temp_file = read_dir(temp_path)

# dir_name = {'Left': [], 'Right': [], 'Center': []}
# for camera in dir_name:
#     dir_name[camera] = [
#         file_path for file_path in temp_file if camera in file_path
#     ]

# for camera in dir_name:
#     for index,name in enumerate(dir_name[camera]):
#         time=
#         name_new=str(index_start+index)+camera+
print(saved_file)