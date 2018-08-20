from torch.utils.data import Dataset, DataLoader
import os
from os.path import dirname,abspath,join
import pandas
import torch



class URPedestrianDataset(Dataset):
    def __init__(self,dataset_dir):
        self.dataset_root=dataset_dir
        self.frame_root=[]
        self.command_root=[]
        self.frame_list = {0: [], 1: [], 2: [], 3: []}
        self.command_list = {0: [], 1: [], 2: [], 3: []}
        for i in range(4):
            video_folder=os.path.join(self.dataset_root,f'video/{i}')
            command_folder=os.path.join(self.dataset_root,f'command/{i}')
            self.frame_root.append(video_folder)
            self.command_root.append(command_folder)
            self.frame_list[i]=self._get_sorted_framelist(video_folder)
            self.command_list=pandas.read_csv(join(command_folder,'all_three.csv'))
    def _get_sorted_framelist(self,path):
        def sort_func(e):
            """video_num,frame,camera"""
            name = os.path.basename(e).replace('.jpg', '').split('_')

            video_num,frame_num,camera_name = int(name[0]),int(name[2]),name[1]
            constant = 1 if camera_name == 'center' else 3 if camera_name == 'left' else 2
            # print(video_num * 1e6 + frame_num * 10 + constant)
            return video_num * 1e6 + frame_num * 10 + constant
        frame = [join(path,file) for file in os.listdir(path) if 'jpg' in file]
        frame.sort(key=sort_func)
        return frame


parent_dir=dirname(dirname(abspath(__file__)))
dataset_path=join(parent_dir,'data/dataset')
a=URPedestrianDataset(dataset_path)
print('hehe')