from typing import List
import numpy as np

class Analyst:
    def __init__(self, test_image_data: dict) -> None:
        self.correct_labels = test_image_data[b"labels"]
    
    def score(self, predictions: np.ndarray) -> float:
        prediction_no= len(predictions)
        return np.sum(predictions == self.correct_labels[:prediction_no]) / prediction_no
