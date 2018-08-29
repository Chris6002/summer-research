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
import copy
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
loader={}
loader['train'] = torch.utils.data.DataLoader(dataset,
                                           batch_size=32, sampler=train_sampler,num_workers=4)

loader['val'] = torch.utils.data.DataLoader(dataset,
                                                batch_size=16, sampler=validation_sampler)
print(len(loader['train']),len(loader['val']))
# =============================================
# Load all used net
# =============================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
net = model.BasicResNet()
if torch.cuda.device_count() > 1:
    print("Let's use", torch.cuda.device_count(), "GPUs!")
    # dim = 0 [30, xxx] -> [10, ...], [10, ...], [10, ...] on 3 GPUs
    net = nn.DataParallel(net).cuda()
else:
    print("Current using "+str(device))
    net=net.to(device)
# =============================================
# Define a Loss function and optimizer
# =============================================

import torch.optim as optim

criterion = nn.CrossEntropyLoss().to(device)
optimizer = optim.Adam(net.parameters(), lr=0.001, betas=(0.9,0.99))


def trainer(dataloader,model,criterion,optimizer,epoch_num=10):
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc=0.0
    for epoch in range(epoch_num):

        print('Epoch {}/{}'.format(epoch, epoch_num))
        print('-' * 10)
        for phase in ['train', 'val']:

            # init
            start_time = time.time()
            size_batch=dataloader[phase].batch_size
            size_data=len(dataloader[phase])
            running_acc=0
            iteration_acc=0
            model.train() if phase == 'train' else model.eval()
            # Iterate over data.
            for index, data in enumerate(dataloader[phase]):
                print(index)
                inputs = data['frame']
                labels = misc.limit_value_tensor(data['steer'] - 976, 0, 999)
                # if torch.cuda.device_count() <= 1:
                #     inputs = inputs.to(device)
                #     labels = labels.to(device)
                inputs = inputs.cuda()
                labels = labels.cuda()


                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, predicted = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)
                    acc=misc.accuracy(predicted,labels,size_batch)
                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()
                running_acc+=acc
                iteration_acc+=acc
                if index % 100 == 99:
                    print('Iteration: {:>5}/{:<5}'.format(index, size_data),end=' ')
                    print('{} Acc: {:.4f}'.format(phase, iteration_acc/100))
                    iteration_acc=0
            epoch_acc=running_acc/size_data
            time_elapsed=time.time()-start_time
            print('-' * 10)
            print('{} complete in {:.0f}m {:.0f}s'.format(phase,time_elapsed // 60, time_elapsed % 60))
            print('Acc: {:.4f}'.format(epoch_acc))
            print('-' * 10)
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
    model.load_state_dict(best_model_wts)
    return model
        
    
# =============================================
# 4. Train the network
# =============================================


model_best=trainer(loader,net,criterion,optimizer,epoch_num=40)





# for epoch in range(2):  # loop over the dataset multiple times
#     running_loss = 0.0
#     for i, data in enumerate(train_loader):
#         # train_loaderprint(i/70000)
#         start_time=time.time()
#         # get the inputs
#         inputs = data['frame']
#         num=misc.limit_value_tensor(data['steer'] - 976,0,999)
#         num=num.to(device)
#         labels = misc.one_hot_embedding(data['steer'] - 976, class_num=1000).double()

#         # labels=F.softmax(labels,dim=1)
#         inputs, labels = inputs.to(device), labels.to(device)
#         # print(onehot.type())

#         # zero the parameter gradients


#         # forward + backward + optimize
#         outputs = net(inputs)

#         #plt.plot(labels.cpu().numpy(),outputs.cpu().detach().numpy())
#         plt.show()
#         _, predicted = torch.max(outputs.data, 1)
#         # print(predicted.cpu().numpy()-num.cpu().numpy())

#         print("epoch:{0},loss:{1}".format(epoch,misc.accuracy(predicted,num,32)))
#         loss = criterion(outputs, num)
#         optimizer.zero_grad()
#         # print("epoch:{0},loss:{1}".format(epoch,loss))
#         loss.backward()

#         optimizer.step()

#         # print statistics
#         running_loss += loss.item()
#         if i % 500 == 499:  # print every 2000 mini-batches
#             print('[%d, %5d] loss: %.3f' %
#                   (epoch + 1, i + 1, running_loss / 500))
#             running_loss = 0.0
#         # print(round(1/(time.time()-start_time)))
# print('Finished Training')
