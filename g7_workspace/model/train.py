import argparse
import copy
import time
from os.path import dirname, abspath, join

import torch
import torch.nn as nn
from torch.utils.data.sampler import SubsetRandomSampler

import misc
import shutil
import model
from dataloader import URPedestrianDataset

parser = argparse.ArgumentParser()
parser.add_argument('--muiltpleGPU', type=int, default=0)
parser.add_argument('--cuda', type=int, default=0)
parser.add_argument('--classnum', type=int, default=0)
args = parser.parse_args()
for arg in vars(args):
    print("Argu:{:>10}:{:<10}".format(arg, getattr(args, arg)))
# =============================================
# Load all used net
# =============================================

net = model.BasicResNet()

device = torch.device(
        f"cuda:{args.cuda}" if torch.cuda.is_available() else "cpu")
if args.muiltpleGPU == 1 and torch.cuda.device_count() > 1:
    print("Let's use", torch.cuda.device_count(), "GPUs!")
    batch_size = 4 * 32
    worker_num = 16
    net = nn.DataParallel(net).cuda()
else:
    print(f"Current using {device}")
    batch_size = 8
    worker_num = 4
    net = net.to(device)
print(f"batch size: {batch_size}, worker number: {worker_num}")
    
# =============================================
# Split dataset
# ^^^^^^^^^^^^^
# Contiguous split
# train_idx, validation_idx = indices[split:], indices[:split]
# =============================================
dataset_path = join(dirname(dirname(abspath(__file__))), 'data/dataset')
dataset = URPedestrianDataset(dataset_path, classnum=args.classnum)
sampler = misc.split_random(dataset.command_list)
loader = {}

loader = {x: torch.utils.data.DataLoader(dataset,
                                         batch_size=batch_size, sampler=sampler[x], num_workers=worker_num) for x in
          ['train', 'val']}

print('train number:{},  val number:{}'.format(
    len(loader['train']), len(loader['val'])))
# =============================================
# Define a Loss function and optimizer
# =============================================

import torch.optim as optim

criterion = nn.CrossEntropyLoss().to(device)
optimizer = optim.Adam(net.parameters(), lr=0.001, betas=(0.9, 0.99))


def train(loader, model, criterion, optimizer, device, log):
    model.train()
    size_batch, size_data = loader.batch_size, len(loader)
    running_acc_20,iteration_acc_20, iteration_acc_50 = 0, 0,0
    for index, data in enumerate(loader):
        inputs = data['frame'].to(device)
        labels = misc.limit_value_tensor(
            data['steer'] - 976, 0, 999).to(device)
        optimizer.zero_grad()
        with torch.set_grad_enabled(True):
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            loss = criterion(outputs, labels)
            acc_50 = misc.accuracy(predicted, labels, size_batch, 20)
            acc_20 = misc.accuracy(predicted, labels, size_batch, 50)
            loss.backward()
            optimizer.step()
        running_acc_20 += acc_20
        iteration_acc_20 += acc_20
        iteration_acc_50 += acc_50
        if index % 100 == 99:
            out='Iteration: {:>5}/{:<5}  {} Acc_20: {:.4f} Acc_50: {:.4f}'.format(index,size_data, 'train', iteration_acc_20 / 100,iteration_acc_50/100)
            print(out)
            log.write(out)
            iteration_acc_20,iteration_acc_50 = 0,0
    return running_acc_20 / size_data


def validate(loader, model, criterion, optimizer, device, log):
    model.eval()
    size_batch, size_data = loader.batch_size, len(loader)
    running_acc_20,iteration_acc_20, iteration_acc_50 = 0, 0,0
    for index, data in enumerate(loader):
        inputs = data['frame'].to(device)
        labels = misc.limit_value_tensor(
            data['steer'] - 976, 0, 999).to(device)
        optimizer.zero_grad()
        with torch.set_grad_enabled(False):
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            loss = criterion(outputs, labels)
            acc_50 = misc.accuracy(predicted, labels, size_batch, 20)
            acc_20 = misc.accuracy(predicted, labels, size_batch, 50)
        running_acc_20 += acc_20
        iteration_acc_20 += acc_20
        iteration_acc_50 += acc_50
        if index % 100 == 99:
            out='Iteration: {:>5}/{:<5}  {} Acc_20: {:.4f} Acc_50: {:.4f}'.format(index,size_data, 'train', iteration_acc_20 / 100,iteration_acc_50/100)
            print(out)
            log.write(out)
            iteration_acc_20,iteration_acc_50 = 0,0
    return running_acc_20 / size_data


def trainer(dataloader, model, criterion, optimizer, args, epoch_num=10, checkpoint=0, device="cuda:0"):
    print('======= Start Training =======')
    best_epoch = 0
    best_acc = 0.0
    recorder = open('acc_result.txt', 'w')
    for epoch in range(epoch_num):
        time_start=time.time()
        print('Epoch {}/{}'.format(epoch, epoch_num))
        print('=' * 40)
        train_acc = train(dataloader['train'], net,
                          criterion, optimizer, device, recorder)
        valid_acc = validate(dataloader['val'], net, criterion,
                             optimizer, device, recorder)
        time_elapsed=time.time()-time_start
        print('-' * 10)
        print('{} complete in {:.0f}m {:.0f}s'.format(
            time_elapsed // 60, time_elapsed % 60))
        output = 'Epoch:{:3} Train Acc={:5}, Val Acc={:5}'.format(
            epoch, train_acc, valid_acc)
        print(output)
        recorder.write(output)
        print('-' * 10)

        
        if valid_acc > best_acc:
            best_acc = valid_acc
            best_epoch = epoch
            is_best = 1
        else:
            is_best = 0
        if checkpoint == 1:
            misc.save_checkpoint({
                'state_dict': model.state_dict(),
                'optimizer': optimizer.state_dict(),
            }, is_best, filename="checkpoint_{:02}.pth.tar".format(epoch))
    recorder.write(f'best epoch: {best_epoch}')
    recorder.close()


# =============================================
# 4. Train the network
# =============================================


trainer(loader, net, criterion, optimizer,args,epoch_num=40, checkpoint=1,device=device)
