import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import numpy as np

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class BasicResNet(nn.Module):
    def __init__(self):
        super(BasicResNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, (15, 20), stride=(4, 5), padding=(4, 6), dilation=(3, 5))
        Resnet = torchvision.models.resnet18(pretrained=True)
        # for param in Resnet.parameters():
        #     param.requires_grad = False
        Resnet.conv1 = self.conv1
        self.Resnet_feature = Resnet

    def forward(self, x):
        x = self.Resnet_feature(x).double()
        # x = F.log_softmax(x,dim=1)

        return x
