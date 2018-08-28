import numpy as np
import torch
from torch.utils.data.sampler import SubsetRandomSampler


def split_random(num_frame):
    indices = list(range(num_frame))
    num_train = round(num_frame * 0.1)
    num_valid = round(num_frame * 0.2)
    valid_idx = np.random.choice(indices, size=num_valid, replace=False)
    train_idx = np.random.choice(list(set(indices) - set(valid_idx)), size=num_train, replace=False)
    train_sampler = SubsetRandomSampler(train_idx)
    validation_sampler = SubsetRandomSampler(valid_idx)
    return train_sampler, validation_sampler

def limit_value(n, minn, maxn):
    return max(min(maxn, n), minn)
def limit_value_tensor(n, minn, maxn):
    buffer=[]
    for i in n:
        buffer.append(max(min(maxn, i.item()), minn))
    return torch.LongTensor(buffer)

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
        index=limit_value(label_list[0],0,999)
        onehot = eye_vec[index].view(1,-1)
    else:
        index = limit_value(label_list[0], 0, 999)
        onehot = eye_vec[index].view(1,-1)
        for i in range(len(label_list)-1):
            index=limit_value(label_list[0], 0, 999)
            label=eye_vec[index].view(1,-1)
            onehot=torch.cat((onehot,label),0)
    return onehot.double()
