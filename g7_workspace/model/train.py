from os.path import dirname, abspath, join
from dataloader import URPedestrianDataset
import matplotlib.pyplot as plt
import torch.nn.functional as F
import numpy as np
import misc
import time
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
dataset = URPedestrianDataset(dataset_path, classnum=0)

train_sampler, validation_sampler = misc.split_random(len(dataset))

train_loader = torch.utils.data.DataLoader(dataset,
                                           batch_size=32, sampler=train_sampler)

validation_loader = torch.utils.data.DataLoader(dataset,
                                                batch_size=2, sampler=validation_sampler)

# =============================================
# Load all used net
# =============================================
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Current using "+str(device))
net = model.BasicResNet().to(device)

# =============================================
# Define a Loss function and optimizer
# =============================================

import torch.optim as optim

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.001, betas=(0.9,0.99))

# =============================================
# 4. Train the network
# =============================================

for epoch in range(2):  # loop over the dataset multiple times
    running_loss = 0.0
    for i, data in enumerate(train_loader):
        # train_loaderprint(i/70000)
        start_time=time.time()
        # get the inputs
        inputs = data['frame']
        num=misc.limit_value_tensor(data['steer'] - 976,0,999)
        num=num.to(device)
        labels = misc.one_hot_embedding(data['steer'] - 976, class_num=1000).double()

        # labels=F.softmax(labels,dim=1)
        inputs, labels = inputs.to(device), labels.to(device)
        # print(onehot.type())

        # zero the parameter gradients


        # forward + backward + optimize
        outputs = net(inputs)

        #plt.plot(labels.cpu().numpy(),outputs.cpu().detach().numpy())
        plt.show()
        _, predicted = torch.max(outputs.data, 1)
        # print(predicted.cpu().numpy()-num.cpu().numpy())

        print("epoch:{0},loss:{1}".format(epoch,misc.accuracy(predicted,num,32)))
        loss = criterion(outputs, num)
        optimizer.zero_grad()
        # print("epoch:{0},loss:{1}".format(epoch,loss))
        loss.backward()

        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 500 == 499:  # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 500))
            running_loss = 0.0
        # print(round(1/(time.time()-start_time)))
print('Finished Training')
# =============================================
# 4. Test the network
# =============================================

correct = 0
total = 0
with torch.no_grad():
    for data in validation_loader:
        images, labels = data['frame'],data['steer'] - 976
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (abs(predicted - labels)<25).sum().item()

print('Accuracy of the network on the 10000 test images: %d %%' % (
        100 * correct / total))
def trainer(dataloader,model,criterion,optimizer,epoch_num=10):
    batch_size=dataloader.batch_size
    running_acc=0
    for phase in ['train', 'val']:
        if phase == 'train':
            model.train()  # Set model to training mode
        else:
            model.eval()  # Set model to evaluate mode

        # Iterate over data.
        for inputs, labels in dataloaders[phase]:
            inputs = inputs.to(device)
            labels = labels.to(device)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward
            # track history if only in train
            with torch.set_grad_enabled(phase == 'train'):
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)

                # backward + optimize only if in training phase
                if phase == 'train':
                    loss.backward()
                    optimizer.step()
    for epoch in range(epoch_num):
        # training:
        start_time=time.time()
        print('Epoch {}/{}'.format(epoch, epoch_num - 1))
        print('-' * 10)
        model.train()
        for index, data in enumerate(dataloader['train']):
            inputs = data['frame'].to(device)
            labels = misc.limit_value_tensor(data['steer'] - 976,0,999).to(device)
            optimizer.zero_grad()
            with torch.set_grad_enabled(True):
                outputs=model(inputs)
                loss=criterion(outputs,labels)
                _, predicted = torch.max(outputs, 1)
                acc=misc.accuracy(predicted,labels,batch_size)
                loss.backward()
                optimizer.step()
                print("epoch:{0},training accuracy:{1}".format(epoch,acc))
            running_acc+=acc
        # eval:
        for index, data in enumerate(dataloader['val']):
            inputs = data['frame'].to(device)
            labels = misc.limit_value_tensor(data['steer'] - 976,0,999).to(device)
        time_elapsed=time.time()-start_time
        print('NO.{:>2} Epoch complete in {:.0f}m {:.0f}s'.format(
            time_elapsed // 60, time_elapsed % 60))

