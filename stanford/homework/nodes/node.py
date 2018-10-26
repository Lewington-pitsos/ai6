import numpy as np

class Node:
    def __init__(self):
        self.output  = None

def confirm_shape(arr: np.ndarray, correct_shape: tuple):
    actual_shape = arr.shape
    if actual_shape != correct_shape:
        raise ValueError("ndarray of shape: {} should have shape: {}".format(actual_shape, correct_shape))