import pickle
import glob
import os

import numpy as np
from skimage.io import imsave

DATA_DIR = "/home/lewington/ai6/stanford/neighbour/cifar-10-batches-py"

def load_batch(batch_name: str) -> dict:
    with open(os.path.join(DATA_DIR, batch_name), "rb") as batch:
        data_dict = pickle.load(batch, encoding="bytes")
    return data_dict

def save_image(directory: str, data_dict: dict, index: int):
    """
        Saves a data blob as an image file.
    """

    img_flat = data_dict[b"data"][index]
    img_name = data_dict[b"filenames"][index].decode("utf-8")

    # consecutive 1024 entries store color channels of 32x32 image 
    img_R = img_flat[0:1024].reshape((32, 32))
    img_G = img_flat[1024:2048].reshape((32, 32))
    img_B = img_flat[2048:3072].reshape((32, 32))
    img = np.dstack((img_R, img_G, img_B))

    imsave(os.path.join(directory, img_name), img)

def setup_preview_dir(test_image_name: str):
    preview_dir = os.path.join("previews", test_image_name.decode("utf-8"))
    img_dir = os.path.join(preview_dir, "test_image")
    prediction_dir = os.path.join(preview_dir, "predictions")
    if not os.path.exists(preview_dir):
        os.makedirs(preview_dir)
        os.makedirs(img_dir)
        os.makedirs(prediction_dir)
    
    return img_dir, prediction_dir
