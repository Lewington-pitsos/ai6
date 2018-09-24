import numpy as np

def l1(
    test_img: np.ndarray, 
    learned_imgs: np.ndarray
) -> np.ndarray:
    return np.sum(
        abs(np.subtract(
            test_img, 
            learned_imgs, 
            dtype=np.int16
        )), 
        axis=1
    )

def l2(
    test_img: np.ndarray, 
    learned_imgs: np.ndarray
) -> np.ndarray:
    print(np.sum(
        np.square(abs(np.subtract(
            test_img, 
            learned_imgs, 
            dtype=np.int16
        ))), 
        axis=1
    ))
    return np.sqrt(np.sum(
        np.square(abs(np.subtract(
            test_img, 
            learned_imgs, 
            dtype=np.int16
        ))), 
        axis=1
    ))