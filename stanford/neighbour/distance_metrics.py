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

def l1v2(
    test_img: np.ndarray, 
    learned_imgs: np.ndarray,
    breadth: int = 5
) -> int:
    distances = l1(test_img, learned_imgs)
    neighbor_indices = np.argpartition(distances, breadth)[:breadth]

    neighbor_neighbor_indices = []

    for neighbor in neighbor_indices:
        neighbor_distances = l1(learned_imgs[neighbor], learned_imgs)
        neighbor_neighbor_indices.append(np.argpartition(distances, breadth)[0])

    print(neighbor_neighbor_indices)

    (indices, counts) = np.unique(neighbor_neighbor_indices, return_counts=True)

    return indices[np.argmax(counts)]

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