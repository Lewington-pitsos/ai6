import nearest
import preview as pv

n = nearest.Nearest()
test_img_data = pv.load_batch("test_batch")
print(n.predict_all(test_img_data))


