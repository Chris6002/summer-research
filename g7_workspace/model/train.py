from os.path import dirname,abspath,join
from dataloader import URPedestrianDataset
parent_dir = dirname(dirname(abspath(__file__)))
dataset_path = join(parent_dir, 'data/dataset')
a = URPedestrianDataset(dataset_path, classnum=0)
print(len(a))
print('hehe')