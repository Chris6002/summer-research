import numpy as np
import torch
from torch.utils.data.sampler import SubsetRandomSampler
import shutil


def save_checkpoint(state, is_best, num,filename='checkpoint.pth.tar'):
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, f'model_best_{num}.pth.tar')


def split_random(command_list):
    train_ratio = 0.7
    valid_ratio = 0.2
    id_list = [[] for i in range(3000)]
    train_idx = []
    valid_idx = []
    for index, steer in enumerate(command_list['steering']):
        id_list[int(steer)].append(index)
    for index, id_num in enumerate(id_list):
        if len(id_num) > 0 and index >= 976 and index < 1976:
            sample_size = len(id_num)
            num_train = round(sample_size * train_ratio)
            num_valid = round(sample_size * valid_ratio)
            # if num_train:
            index_list = np.random.choice(
                id_num, size=num_train, replace=False)
            if len(index_list) > 0:
                for i in index_list:
                    train_idx.append(i)
            #  numif_valid > 0:

            if len(list(set(id_num)-set(train_idx))) > 0:
                index_list = np.random.choice(
                    list(set(id_num)-set(train_idx)), size=num_valid, replace=False)
                for i in index_list:
                    valid_idx.append(i)
    train_sampler = SubsetRandomSampler(train_idx)
    validation_sampler = SubsetRandomSampler(valid_idx)
    sampler = {}
    sampler['train'] = train_sampler
    sampler['val'] = validation_sampler
    return sampler


def limit_value(n, minn, maxn):
    return max(min(maxn, n), minn)


def limit_value_tensor(n, minn, maxn):
    buffer = []
    for i in n:
        buffer.append(max(min(maxn, i.item()), minn))
    return torch.LongTensor(buffer)


def accuracy(predicted, true, batch_size, top):
    correct = (abs(predicted - true) < top/2).sum().item()
    return round(correct/batch_size*100, 2)


def one_hot_embedding(label_list, class_num):
    """Embedding labels to one-hot form.

    Args:
      labels: (LongTensor) class labels, sized [N,].
      num_classes: (int) number of classes.

    Returns:
      (tensor) encoded labels, sized [N, #classes].
    """

    eye_vec = torch.eye(class_num)
    if len(label_list) == 1:
        index = limit_value(label_list[0], 0, 999)
        onehot = eye_vec[index].view(1, -1)
    else:
        index = limit_value(label_list[0], 0, 999)
        onehot = eye_vec[index].view(1, -1)
        for i in range(len(label_list)-1):
            index = limit_value(label_list[0], 0, 999)
            label = eye_vec[index].view(1, -1)
            onehot = torch.cat((onehot, label), 0)
    return onehot.double()
