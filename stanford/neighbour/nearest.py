import numpy as np
import preview as pv
from typing import List

PRED_NO = 100

class Nearest:
    def __init__(self):
        self.train()

    def train(self):
        self.labels = pv.load_batch("batches.meta")[b"label_names"]
        self.data = pv.load_batch("data_batch_1")
        self.example_img = self.data[b"data"][0]

    def predict_all(
        self, 
        test_image_data: dict, 
        preview: bool = False
    ) -> np.ndarray:
        test_images = test_image_data[b"data"]
        predictions = np.zeros(PRED_NO)
        for index, flat_img in enumerate(test_images):
            if index >= PRED_NO:
                break

            prediction_indices = self.get_similar_image_indices(flat_img)

            if preview:
                self.preview_predictions(
                    prediction_indices,
                    test_image_data,
                    index
                )

            predictions[index] = self.data[b"labels"][prediction_indices[0]]
            
        return predictions

    def get_similar_image_indices(self, test_img: np.ndarray, number: int = 1) -> List[int]:
        if (
            test_img.ndim != 1 or 
            test_img.shape[0] != self.example_img.shape[0]
        ):
            return []
        
        distances = np.sum(
            abs(np.subtract(
                test_img, 
                self.data[b"data"], 
                dtype=np.int16
            )), 
            axis=1
        )

        return np.argpartition(distances, number)[:number]

    def preview_predictions(
        self,
        prediction_indices: List[int], 
        test_image_data: dict,
        index: int
    ):
        img_dir, prediction_dir = pv.setup_preview_dir(test_image_data[b"filenames"][index])

        pv.save_image(img_dir, test_image_data, index)
        for prediction_index in prediction_indices:
            pv.save_image(prediction_dir, self.data, prediction_index)


        
