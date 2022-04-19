from os import path

import numpy as np
import random

import torch
from torch.utils.data import DataLoader, TensorDataset

# from vibr import constants
import src.vibr.constants as constants


def load(data_dir: str = constants.DATA_DIR):
    # Grab the feature file and moods targets from listening moods data
    features = np.load(path.join(data_dir, 'tp_source_trimmed.npy'), allow_pickle=True)
    moods = np.load(path.join(data_dir, f'moods_target_trimmed.npy'), allow_pickle=True)
    moods = np.stack(moods[:, 1]).astype(float)

    idx = list(range(features.shape[0]))
    random.shuffle(idx)
    features = features[idx]
    moods = moods[idx]

    # TODO:
    #     TITLE: Uncomment to use shared splits
    #     AUTHOR: frndlytm
    #
    # # Grab the cached indexes from the listening-moods training
    # train_idxs, val_idxs, test_idxs = (
    #     np.load(path.join(datadir, f'train_idx.npy')),
    #     np.load(path.join(datadir, f'val_idx.npy')),
    #     np.load(path.join(datadir, f'test_idx.npy')),
    # )
    size = int(features.shape[0])
    train_size, valid_size, test_size = (
        int(0.6 * size), int(0.2 * size), int(0.2 * size),
    )
    train_idxs, val_idxs, test_idxs = (
        slice(0, train_size, 1),
        slice(train_size, train_size+valid_size, 1),
        slice(train_size+valid_size, -1, 1),
    )

    # RETURN DataLoader batch iterators on the data
    return {
        "d_in": features.shape[1],
        "d_out": moods.shape[1],
        "datasets":{
            "train": TensorDataset(
                torch.from_numpy(features[train_idxs]),
                torch.from_numpy(moods[train_idxs])
            ),
            "validate": TensorDataset(
                torch.from_numpy(features[val_idxs]),
                torch.from_numpy(moods[val_idxs])
            ),
            "test": TensorDataset(
                torch.from_numpy(features[test_idxs]),
                torch.from_numpy(moods[test_idxs])
            ),
        },
    }


