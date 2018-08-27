import numpy as np
import torch
from torch.utils.data.sampler import SubsetRandomSampler


def split_random(num_frame):
    indices = list(range(num_frame))
    num_train = round(num_frame * 0.7)
    num_valid = round(num_frame * 0.2)
    valid_idx = np.random.choice(indices, size=num_valid, replace=False)
    train_idx = np.random.choice(list(set(indices) - set(valid_idx)), size=num_train, replace=False)
    train_sampler = SubsetRandomSampler(train_idx)
    validation_sampler = SubsetRandomSampler(valid_idx)
    return train_sampler, validation_sampler


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
        onehot = eye_vec[label_list[0]].view(1,-1)
    else:
        onehot = eye_vec[label_list[0]].view(1,-1)
        for i in range(len(label_list)-1):
            label=eye_vec[label_list[i+1]].view(1,-1)
            onehot=torch.cat((onehot,label),0)
    return onehot.double()
