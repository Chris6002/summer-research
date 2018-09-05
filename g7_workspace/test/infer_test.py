from director import Monitor
from PIL import Image
import os
import torchvision.transforms as transforms

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--image', type=str )
parser.add_argument('--model', type=str )
args = parser.parse_args()

from PIL import Image


# rotated_image.save(saved_location)
# rotated_image.show()
dir_path = os.path.dirname(os.path.realpath(__file__))
frames_folder=os.path.join(dir_path,'frames')

frames_list=[os.path.join(frames_folder,name) for name in os.listdir(frames_folder) if '.jpg' in name]
# for index,path in enumerate(frames_list):
#
#     print(path)
#     Image.open(path)
#
monitor=Monitor(args.model)


# transform = transforms.Compose([transforms.ToTensor()])
# frame=Image.open(args.image)
# rotated_image = frame.transpose(Image.FLIP_LEFT_RIGHT)
# frame=transform(frame)
for index,path in enumerate(frames_list):
    frame=Image.open(path)
    output=monitor.inference(frame)
    turn=os.path.basename(path).split('_')[-1].split('.')[0]
    print("{:>20}   ===>   {:4}".format(os.path.basename(path),output.item()),end= "   ")
    predicted='right' if output.item()>1500 else 'left' if output.item()<1460 else 'center'
    print('O') if predicted==turn else print('X')