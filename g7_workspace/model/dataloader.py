from torch.utils.data import Dataset, DataLoader
import os
import torchvision.transforms as transforms
import pandas
import numpy as np
from PIL import Image



class URPedestrianDataset(Dataset):
    def __init__(self, dataset_dir, classnum=0,dagger=1):
        self.transform = transforms.Compose([transforms.ToTensor()])
        self.dataset_root = dataset_dir
        # / home / vision / summer - research / g7_workspace / data / dataset
        # / home / vision / summer - research / g7_workspace / data / dagger
        if dagger == 0:

            print(self.dataset_root)
            self.frame_root = []
            self.command_root = []


            video_folder = os.path.join(self.dataset_root, f'video/{classnum}')
            command_folder = os.path.join(self.dataset_root, f'command/{classnum}')
            self.frame_root = video_folder
            self.command_root = command_folder
            self.frame_list = self._get_sorted_framelist(video_folder)
            if os.path.exists(os.path.join(command_folder, 'all_three.csv')):
                print(os.path.join(command_folder, 'all_three.csv'))

        else:
            video_folder=os.path.join(self.dataset_root, f'{classnum}/video')
            command_folder = os.path.join(self.dataset_root, f'{classnum}/command')
            self.frame_root = video_folder
            self.command_root = command_folder
            self.command_list = pandas.read_csv(os.path.join(command_folder, '1.csv'))

    def _get_sorted_framelist(self, path):
        def sort_func(e):
            """video_num,frame,camera"""
            name = os.path.basename(e).replace('.jpg', '').split('_')

            video_num, frame_num, camera_name = int(name[0]), int(name[2]), name[1]
            constant = 1 if camera_name == 'center' else 3 if camera_name == 'left' else 2
            # print(video_num * 1e6 + frame_num * 10 + constant)
            return video_num * 1e6 + frame_num * 10 + constant

        frame = [os.path.join(path, file) for file in os.listdir(path) if 'jpg' in file]
        frame.sort(key=sort_func)
        return frame

    def __len__(self):
        if len(self.frame_list) == len(self.command_list):
            return len(self.command_list)
        else:
            print('command frame not match')
            return min(len(self.frame_list), len(self.command_list))

    def __getitem__(self, item):
        name=self.command_list.iloc[item]['name']
        frame = self.command_list.iloc[item]['frame']
        label=self.command_list.iloc[item]['steering']
        # ===========================================================================
        noise_label= np.random.normal(int(label) , 20, 1)
        path=os.path.join(self.frame_root, f"{name}_{frame:06d}.jpg")
        frame=Image.open(path)
        sample={'frame':self.transform(frame),'steer':label,'noise_label':noise_label}
        return sample



