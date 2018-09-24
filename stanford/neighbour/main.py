import nearest
import preview as pv

n = nearest.Nearest()
test_img_data = pv.load_batch("test_batch")
n.predict_all(test_img_data)


