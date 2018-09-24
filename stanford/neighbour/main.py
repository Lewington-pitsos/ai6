import nearest
import analyst
import preview as pv

n = nearest.Nearest()
test_img_data = pv.load_batch("test_batch")
a = analyst.Analyst(test_img_data)
predictions = n.predict_all(test_img_data)
print(predictions)


print(a.score(predictions))


