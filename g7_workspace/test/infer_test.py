from director import Monitor
from PIL import Image

import torchvision.transforms as transforms

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str )

args = parser.parse_args()


transform = transforms.Compose([transforms.ToTensor()])
frame=Image.open(args.path)
# frame=transform(frame)
monitor=Monitor('./model_best.pth.tar')
output=monitor.inference(frame)
print(output.item())