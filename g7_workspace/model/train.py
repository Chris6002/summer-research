import argparse
import copy
import time
from os.path import dirname, abspath, join

import torch
import torch.nn as nn
from torch.utils.data.sampler import SubsetRandomSampler

import misc
import model
from dataloader import URPedestrianDataset

parser = argparse.ArgumentParser()
parser.add_argument('--muiltpleGPU', type=int, default=0)
parser.add_argument('--cuda', type=int, default=0)
parser.add_argument('--classnum',type=int,default=0)
args = parser.parse_args()
for arg in vars(args):
    print ("Argu:{:>10}:{:<10}".format(arg,getattr(args, arg)))
# =============================================
# Load all used net
# =============================================

net = model.BasicResNet()


if args.muiltpleGPU == 1 and torch.cuda.device_count() > 1:
    print("Let's use", torch.cuda.device_count(), "GPUs!")
    batch_size = 4 * 32
    worker_num = 16
    net = nn.DataParallel(net,device_ids=args.muiltpleGPU).cuda()
else:
    device = torch.device(
        f"cuda:{args.cuda}" if torch.cuda.is_available() else "cpu")
    print(f"Current using {device}")
    batch_size = 8
    worker_num = 4
    print(f"batch size: {batch_size}, worker number: {worker_num}")
    net = net.to(device)
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


def trainer(dataloader, model, criterion, optimizer, epoch_num=10, checkpoint=0):
    print('======= Start Training =======')
    best_model_wts = copy.deepcopy(model.state_dict()).to(device)
    best_acc = 0.0
    recorder = open('acc_result.txt', 'w')
    for epoch in range(epoch_num):

        print('Epoch {}/{}'.format(epoch, epoch_num))
        print('=' * 40)
        for phase in ['train', 'val']:

            # init
            start_time = time.time()
            size_batch = dataloader[phase].batch_size
            size_data = len(dataloader[phase])
            running_acc = 0
            iteration_acc = 0
            model.train() if phase == 'train' else model.eval()
            # Iterate over data.
            for index, data in enumerate(dataloader[phase]):

                inputs = data['frame']
                labels = misc.limit_value_tensor(data['steer'] - 976, 0, 999)
                # if torch.cuda.device_count() <= 1:
                #     inputs = inputs.to(device)
                #     labels = labels.to(device)
                if args.muiltpleGPU:
                    inputs = inputs.cuda()
                    labels = labels.cuda()
                else:
                    inputs = inputs.to(device)
                    labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, predicted = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)
                    acc = misc.accuracy(predicted, labels, size_batch)
                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()
                running_acc += acc
                iteration_acc += acc
                if index % 100 == 99:
                    print(
                        'Iteration: {:>5}/{:<5}'.format(index, size_data), end=' ')
                    print('{} Acc: {:.4f}'.format(phase, iteration_acc / 100))
                    iteration_acc = 0
            if phase == 'train' and checkpoint == 1:
                misc.save_checkpoint({
                    'epoch': epoch + 1,
                    'state_dict': model.state_dict(),
                    'optimizer': optimizer.state_dict(),
                }, 0, filename="checkpoint_{:02}.pth.tar".format(epoch))
            epoch_acc = running_acc / size_data
            time_elapsed = time.time() - start_time
            print('-' * 10)
            print('{} complete in {:.0f}m {:.0f}s Acc:{:.4f}'.format(
                phase, time_elapsed // 60, time_elapsed % 60, epoch_acc))
            recorder.write('{} complete in {:.0f}m {:.0f}s Acc:{:.4f}'.format(
                phase, time_elapsed // 60, time_elapsed % 60, epoch_acc))
            print('-' * 10)
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
    recorder.close()
    model.load_state_dict(best_model_wts)
    return model


# =============================================
# 4. Train the network
# =============================================


model_best = trainer(loader, net, criterion, optimizer,
                     epoch_num=40, checkpoint=1)
misc.save_checkpoint({
    'state_dict': model_best.state_dict(),
    'optimizer': optimizer.state_dict(),
}, 1)
