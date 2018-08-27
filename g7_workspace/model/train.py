from os.path import dirname,abspath,join
from dataloader import URPedestrianDataset
import numpy as np
import misc
import torch
import model
import torch.nn as nn
from torch.utils.data.sampler import SubsetRandomSampler
import torch.nn.functional as F


dataset_path = join(dirname(dirname(abspath(__file__))), 'data/dataset')




# =============================================
# Split dataset
# ^^^^^^^^^^^^^
# Contiguous split
# train_idx, validation_idx = indices[split:], indices[:split]
# =============================================
dataset=URPedestrianDataset(dataset_path, classnum=0)
print(len(dataset))
train_sampler,validation_sampler=misc.split_random(len(dataset))

train_loader = torch.utils.data.DataLoader(dataset,
                batch_size=4, sampler=train_sampler)

validation_loader = torch.utils.data.DataLoader(dataset,
                batch_size=2, sampler=validation_sampler)



# =============================================
# Load all used net
# =============================================

net=model.BasicResNet()


# =============================================
# Define a Loss function and optimizer
# =============================================

import torch.optim as optim

criterion = nn.KLDivLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)


# =============================================
# 4. Train the network
# =============================================

for epoch in range(2):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(train_loader):
        # get the inputs
        inputs = data['frame']
        labels=data['steer']-976
        onehot=misc.one_hot_embedding(labels,1000).double()
        print(onehot.type())

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, onehot)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 2000 == 1999:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0

print('Finished Training')
# =============================================
# 4. Test the network
# =============================================

correct = 0
total = 0
with torch.no_grad():
    for data in validation_loader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print('Accuracy of the network on the 10000 test images: %d %%' % (
    100 * correct / total))