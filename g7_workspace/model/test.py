import torch
# from torchvision import models
#
# Resnet = models.resnet18(pretrained=True)
# # print(Resnet)
# for i,child in enumerate(Resnet.children()):
#     print(i,child)
# image = torch.zeros(1, 3, 224, 224)
# print(Resnet.conv1(image).shape)
# image = torch.zeros(1, 3, 640, 480)
# conv = torch.nn.Conv2d(3, 64, (20, 15), stride=(5, 4), padding=(6, 4), dilation=(5,3))
# out = conv(image)
# print(out.shape)

# import torch.nn.functional as F
# loss_kl = torch.nn.KLDivLoss(reduction='sum')
# loss_ce=torch.nn.CrossEntropyLoss()
# batch_size = 5
# input=torch.randn(batch_size, 10)
# target=torch.randn(batch_size, 10)
# log_probs1 = F.log_softmax(input, 1)
# probs2 = F.softmax(target, 1)
# print(loss_kl(log_probs1, probs2) / batch_size)
# a=torch.empty(3, dtype=torch.long).random_(5)
# print(loss_ce(input,target))

# import misc
# a=[0,1,2]
# print(misc.one_hot_embedding(a,3)).

# ===============================================================
# f=open('/home/vision/summer-research/g7_workspace/model/result.txt')
# a,b=[],[]
# for i,line in enumerate(f.readlines()):
#     if line.split(':')[0]=='Acc':
#         acc=line.split(':')[1]
#         # print(acc)
#         if i%2==1:
#             a.append(float(acc.strip()))
#         else:
#             b.append(flo+at(acc.strip()))
# print(a,b)
# import matplotlib.pyplot as plt
# import numpy as np
# plt.plot(b)
# plt.ylim(0,100)
# plt.show()
# =======================================================================

# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('--integer', type=int,default=10, help='display an integer')
# args = parser.parse_args()

# print (args.integer)

# import matplotlib as mpl
# mpl.use('TkAgg')  # or whatever other backend that you want
# import matplotlib.pyplot as plt
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--muiltpleGPU', type=0, default=0)
parser.add_argument('--cuda', type=int, default=0)
parser.add_argument('--classnum',type=int,default=0)
args = parser.parse_args()
for arg in vars(args):
    print(arg,getattr(args,arg))
    # print ("Argu:{:>10}:{:<10}".format(arg,getattr(args, arg)))