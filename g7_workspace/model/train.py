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
#  $ python train.py --muiltGPU 0 1  --classnum 0 --batch_size 128
#  $ python train.py --single 0  --classnum 0 --batch_size 128

parser = argparse.ArgumentParser()
parser.add_argument('--muiltGPU',  nargs='+',type=int, default=[0])
parser.add_argument('--singleGPU', type=int, default=0)
parser.add_argument('--classnum', type=int, default=0)
parser.add_argument('--batch_size',type=int,default=64)
parser.add_argument('--worker_num',type=int,default=16)
parser.add_argument('--resume',type=str,default='None')
args = parser.parse_args()
for arg in vars(args):
    print("{:>13}:{}".format(arg, getattr(args, arg)))
# =============================================
# Load all used net
# =============================================
net = model.BasicResNet()
if args.resume != 'None':
    parameter=torch.load(args.resume,map_location=lambda storage, loc: storage)
    net.load_state_dict(parameter['state_dict'])
    if 'epoch' in parameter:
        print('starting at epoch: ',parameter['epoch'])
    else:
        print('starting from unknown')

if len(args.muiltGPU) > 1 and torch.cuda.device_count() > 1:
    device = torch.device(
        f"cuda:{args.muiltGPU[0]}" if torch.cuda.is_available() else "cpu")
    print("Let's use", len(args.muiltGPU), "GPUs!")
    batch_size = args.batch_size*len(args.muiltGPU)
    worker_num = args.worker_num
    net = nn.DataParallel(net,device_ids=args.muiltGPU).to(device)
    criterion = nn.CrossEntropyLoss().to(device)

    # criterion=nn.DataParallel(nn.CrossEntropyLoss(),device_ids=args.muiltGPU).to(device)
else:
    device = torch.device(
        f"cuda:{args.singleGPU}" if torch.cuda.is_available() else "cpu")
    print(f"Current using {device}")
    batch_size = args.batch_size
    worker_num = 16
    net = net.to(device)
    criterion = nn.CrossEntropyLoss().to(device)

print(f"batch size: {batch_size}, worker number: {worker_num}")

# =============================================
# Split dataset
# ^^^^^^^^^^^^^
# Contiguous split
# train_idx, validation_idx = indices[split:], indices[:split]
# =============================================
dataset_path = join(dirname(dirname(abspath(__file__))), 'data/dataset')
dataset = URPedestrianDataset(dataset_path, csv_name='test.csv',classnum=args.classnum,dagger=0)
#################### DAGGER ==========================================
# dataset_path = join(dirname(dirname(abspath(__file__))), 'data/dagger')
# dataset = URPedestrianDataset(dataset_path, csvname='1.csv' classnum=args.classnum,dagger=1)
#============================================================================
sampler = misc.split_random(dataset.command_list)
loader = {}

loader = {x: torch.utils.data.DataLoader(dataset,
                                         batch_size=batch_size, sampler=sampler[x], num_workers=worker_num) for x in
          ['train', 'val']}

print('train batch #:{},  val batch #:{}'.format(
    len(loader['train']), len(loader['val'])))
print('train #:{},  val #:{}'.format(
    len(loader['train'])*batch_size, len(loader['val'])*batch_size))
# =============================================
# Define a Loss function and optimizer
# =============================================


import torch.optim as optim
optimizer = optim.Adam(net.parameters(), lr=0.001, betas=(0.9, 0.99))


def train(loader, model, criterion, optimizer, device, log):
    model.train()
    size_batch, size_data = loader.batch_size, len(loader)
    running_acc_20, iteration_acc_20, iteration_acc_50 = 0, 0, 0
    for index, data in enumerate(loader):

        inputs = data['frame'].to(device)
        labels = misc.limit_value_tensor(
            data['noise_label'] - 976, 0, 999).to(device)
        real_label=misc.limit_value_tensor(
            data['steer'] - 976, 0, 999).to(device)

        optimizer.zero_grad()
        with torch.set_grad_enabled(True):
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            loss = criterion(outputs, labels)
            acc_50 = misc.accuracy(predicted, real_label, size_batch, 20)
            acc_20 = misc.accuracy(predicted, real_label, size_batch, 50)
            loss.backward()
            optimizer.step()
        running_acc_20 += acc_20
        iteration_acc_20 += acc_20
        iteration_acc_50 += acc_50
        if index % 100 == 99:
            out = 'Iteration: {:>5}/{:<5}  {:5}  || Acc_20: {:.4f}   Acc_50: {:.4f}'.format(
                index, size_data, 'train', iteration_acc_20 / 100, iteration_acc_50/100)
            print(out)
            log.write(out)
            iteration_acc_20, iteration_acc_50 = 0, 0
    return running_acc_20 / size_data


def validate(loader, model, criterion, optimizer, device, log):
    model.eval()
    size_batch, size_data = loader.batch_size, len(loader)
    running_acc_20, iteration_acc_20, iteration_acc_50 = 0, 0, 0
    for index, data in enumerate(loader):
        inputs = data['frame'].to(device)
        labels = misc.limit_value_tensor(
            data['noise_label'] - 976, 0, 999).to(device)
        real_label=misc.limit_value_tensor(
            data['steer'] - 976, 0, 999).to(device)
        optimizer.zero_grad()
        with torch.set_grad_enabled(False):
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            loss = criterion(outputs, labels)
            acc_50 = misc.accuracy(predicted, real_label, size_batch, 20)
            acc_20 = misc.accuracy(predicted, real_label, size_batch, 50)
        running_acc_20 += acc_20
        iteration_acc_20 += acc_20
        iteration_acc_50 += acc_50
        if index % 100 == 99:
            out = 'Iteration: {:>5}/{:<5}  {:5}  || Acc_20: {:.4f}   Acc_50: {:.4f}'.format(
                index, size_data, 'val', iteration_acc_20 / 100, iteration_acc_50/100)
            print(out)
            log.write(out)
            iteration_acc_20, iteration_acc_50 = 0, 0
    return running_acc_20 / size_data


def trainer(dataloader, model, criterion, optimizer, args, epoch_num=10, checkpoint=0, device="cuda:0"):
    print('======= Start Training =======')
    best_epoch = 0
    best_acc = 0.0
    recorder = open('acc_result.txt', 'w')
    for epoch in range(epoch_num):

        time_start = time.time()
        print('Epoch {}/{}'.format(epoch, epoch_num))
        print('=' * 40)
        train_acc = train(dataloader['train'], net,
                          criterion, optimizer, device, recorder)
        valid_acc = validate(dataloader['val'], net, criterion,
                             optimizer, device, recorder)
        time_elapsed = time.time()-time_start
        print('-' * 10)
        print('complete in {:.0f}m {:.0f}s'.format(
            time_elapsed // 60, time_elapsed % 60))
        output = 'Epoch:{:3}    Train Acc={:.3f}, Val Acc={:3f}'.format(
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
                'epoch':epoch+1,
                'state_dict': model.state_dict(),
                'optimizer': optimizer.state_dict(),
            }, is_best, num=args.classnum,filename="checkpoint_{:02}_{:1}.pth.tar".format(epoch,args.classnum))
    recorder.write(f'best epoch: {best_epoch}')
    recorder.close()


# =============================================
# 4. Train the network
# =============================================


trainer(loader, net, criterion, optimizer, args,
        epoch_num=50, checkpoint=1, device=device)
