from director import Monitor
from PIL import Image

import torchvision.transforms as transforms

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str )

args = parser.parse_args()

from PIL import Image


# rotated_image.save(saved_location)
# rotated_image.show()


transform = transforms.Compose([transforms.ToTensor()])
frame=Image.open(args.path)
# rotated_image = frame.transpose(Image.FLIP_LEFT_RIGHT)
# frame=transform(frame)
monitor=Monitor('./0_225_50.pth.tar')
output=monitor.inference(frame)
print(output.item())