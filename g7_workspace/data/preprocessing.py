import os
import subprocess
import shutil
import zipfile
import csv
import zipfile


class DataPath:
    def __init__(self, root):
        self.root = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), root)
        self.video_root = os.path.join(self.root, 'video')
        self.command_root = os.path.join(self.root, 'command')
        self.category = [0, 1, 2, 3]
        self.video_list = {0: [], 1: [], 2: [], 3: [],'root':{}}
        self.command_list = {0: [], 1: [], 2: [], 3: [],'root':{}}
        for num in self.category:
            create_folder(os.path.join(self.video_root, str(num)))
            create_folder(os.path.join(self.command_root, str(num)))
        for i in os.listdir(self.video_root):
            try:
                classnum = int(i)
                self.video_list['root'][classnum]=os.path.join(self.video_root,str(classnum))
                self.command_list['root'][classnum]=os.path.join(self.command_root, str(classnum))
                self.video_list[classnum] = [
                    os.path.join(self.video_list['root'][classnum],path)
                    for path in os.listdir(os.path.join(self.video_root, i))
                    if 'avi' in path
                ]
                self.video_list[classnum].sort(
                    key=lambda x: int(x.split('/')[-1].split('.')[0][0]))
                self.command_list[classnum] = [
                    os.path.join(self.command_list['root'][classnum], path)
                    for path in os.listdir(os.path.join(self.command_root, i))
                    if 'csv' in path
                ]
                self.command_list[classnum].sort(
                    key=lambda x: int(x.split('/')[-1].split('.')[0][0]))
            except:
                pass
    def update(self):
        for i in os.listdir(self.video_root):
            try:
                classnum = int(i)
                self.video_list['root'][classnum]=os.path.join(self.video_root,str(classnum))
                self.command_list['root'][classnum]=os.path.join(self.command_root, str(classnum))
                self.video_list[classnum] = [
                    os.path.join(self.video_list['root'][classnum],path)
                    for path in os.listdir(os.path.join(self.video_root, i))
                    if 'avi' in path
                ]
                self.video_list[classnum].sort(
                    key=lambda x: int(x.split('/')[-1].split('.')[0][0]))
                self.command_list[classnum] = [
                    os.path.join(self.command_list['root'][classnum], path)
                    for path in os.listdir(os.path.join(self.command_root, i))
                    if 'csv' in path
                ]
                self.command_list[classnum].sort(
                    key=lambda x: int(x.split('/')[-1].split('.')[0][0]))
            except:
                pass


# ==========================================================================
# Misc short function
# ==========================================================================


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


def split_name(path):
    """xxx/xxx/1_center.avi -> 1_center"""
    return path.split('/')[-1].split('.')[0]


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def sort_func(e):
    """video_num,frame,camera"""
    name = e.replace('.jpg', '').split('_')
    video_num = int(name[0])
    frame_num = int(name[2])
    camera_name = name[1]
    constant = 1 if camera_name == 'center' else 3 if camera_name == 'left' else 2
    return video_num * 1e6 + frame_num * 10 + constant


def get_start_index(video_path):
    create_folder(video_path)
    saved_file = read_dir(video_path)
    return max(
        map(int, [name.split('/')[-1].split('_')[0]
                  for name in saved_file])) + 1 if saved_file else 1

def get_sorted_frame(path):
    frame = [file for file in os.listdir(path) if 'jpg' in file]
    frame.sort(key=sort_func)
    return frame

# ==========================================================================
# Major function
# ==========================================================================
def unzip_dataset(temp_path):
    while True:
        zipfiles = [zipf for zipf in os.listdir(temp_path) if 'zip' in zipf]
        if len(zipfiles) > 0:
            for name in zipfiles:
                file_path = temp_path + '/' + name
                f = zipfile.ZipFile(file_path)
                print('extracing:  ' + name)
                f.extractall(temp_path)
                f.close()
                os.remove(file_path)
        else:
            print("No zip files in {0}".format(temp_path))
            break


def extract_data(index_start, current_folder, classnum):
    video_root = current_folder + '/video/' + str(classnum)
    create_folder(video_root)
    command_root = current_folder + '/command/' + str(classnum)
    create_folder(command_root)
    temp_path = current_folder + '/temp/' + str(classnum)
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
            command_name = name.replace('Centre', 'Command')
            command_name = command_name.replace('.avi', '_command.csv')
            centre_videoname_new = video_root + name_base + 'center' + '.avi'
            left_videoname_new = video_root + name_base + 'left' + '.avi'
            right_videoname_new = video_root + name_base + 'right' + '.avi'
            commname_new = command_root + name_base + 'center' + '.csv'
            os.rename(command_name, commname_new)
            os.rename(centre_video_name, centre_videoname_new)
            os.rename(left_video_name, left_videoname_new)
            os.rename(right_video_name, right_videoname_new)
    import shutil
    shutil.rmtree(temp_path)
    os.mkdir(temp_path)


def extract_frames(video, dst):
    with open(os.devnull, "w") as ffmpeg_log:
        # if os.path.exists(dst):
        #     print(" cleanup: " + dst + "/")
        #     shutil.rmtree(dst)
        # os.makedirs(dst)
        video_to_frames_command = [
            "ffmpeg",
            # (optional) overwrite output file if it exists
            '-y',
            '-i',
            video,  # input file
            '-qscale:v',
            "2",  # quality for JPEG
            '{0}_%06d.jpg'.format(dst)
        ]
        subprocess.call(
            video_to_frames_command, stdout=ffmpeg_log, stderr=ffmpeg_log)


def sync_frame(path):
    frame = [file for file in os.listdir(path) if 'jpg' in file]
    frame.sort(key=sort_func)
    def get_index(path):
        return path.split('_')[0] + '_' + path.split('_')[1]
    if frame:
        # a=1,2,3,4
        # b=left center right
        a, b = set(), set()
        for file_name in frame:
            a.add(file_name.split('_')[0])
            b.add(file_name.split('_')[1])
        a=sorted(a)
        sync = {}
        for num in a:
            sync.clear()
            for i, camera in enumerate(b):
                index = num + '_' + camera
                # camera_num = index if camera == 'center' else 0
                sync[camera] = [path for path in frame if index == get_index(path) ]

                print("{:>2}_{:8} frame:{:>8}".format(num,camera,len(sync[camera])))
            if len(sync['center']) != len(sync['left']):
                dis = len(sync['left']) - len(sync['center'])
                print(num,end='  ')
                print('left  is more: ' + str(dis))
                for file in sync['left'][-dis:]:
                    print('Sync files: ',path + '/' + file)
                    os.remove(path + '/' + file)

            if len(sync['center']) != len(sync['right']):

                dis = len(sync['right']) - len(sync['center'])
                print(num,end='  ')
                print('right is more: ' + str(dis))
                for file in sync['right'][-dis:]:
                    print('Sync files: ',path + '/' + file)
                    os.remove(path + '/' + file)
                
    else:
        print("No frame in {0}".format(path))


def csv_merge(inputcsv_list, outputcsv):
    with open(inputcsv_list[0]) as csv_file,open(outputcsv, 'w') as out_file:
        csv_reader = csv.DictReader(csv_file)
        new_header = ['name'] + csv_reader.fieldnames
        csv_writer = csv.DictWriter(out_file, new_header)
        csv_writer.writeheader()
    with open(outputcsv, 'a') as out_file:
        for index, inputcsv in enumerate(inputcsv_list):
            with open(inputcsv) as csv_file:
                video_name = inputcsv.split('/')[-1].split('.')[0]
                csv_reader = csv.DictReader(csv_file)
                new_header = ['name'] + csv_reader.fieldnames
                csv_writer = csv.DictWriter(out_file, new_header)
                for row in csv_reader:
                    csv_writer.writerow(dict(row, name=video_name))



def csv_addlr(inputcsv, outputcsv, shift_angel):
    """append left and right command by shifting"""
    with open(inputcsv) as csv_file, open(outputcsv, 'w') as out_file:
        csv_reader = csv.DictReader(csv_file)
        csv_writer = csv.DictWriter(out_file, csv_reader.fieldnames)
        csv_writer.writeheader()
        for row in csv_reader:

            new_left, new_right = row.copy(), row.copy()
            name = row['name']
            steering = row['steering']
            new_left['name'] = name.replace('center', 'left')
            new_right['name'] = name.replace('center', 'right')
            new_left['steering'] = str(int(steering) + shift_angel)
            new_right['steering'] = str(int(steering) - shift_angel)
            csv_writer.writerow(row)
            csv_writer.writerow(new_right)
            csv_writer.writerow(new_left)
