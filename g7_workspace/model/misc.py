import numpy as np

def split_random(num_frame):

    indices=list(range(num_frame))
    num_train=num_frame*0.7
    num_valid=num_frame*0.2
    valid_idx = np.random.choice(indices, size=num_valid, replace=False)
    train_idx =np.random.choice(list(set(indices) - set(valid_idx)), size=num_train, replace=False)
    return valid_idx,train_idx
