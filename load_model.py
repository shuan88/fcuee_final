from tds import * 
import joblib

data0_name = "realdata/needle_100.npy"
data_lable_0 = TDS7_feature(data0_name,1024)
data_pca = np.vstack([data_lable_0[:,:,0],
                      data_lable_0[:,:,1],
                      data_lable_0[:,:,2]])

data_pca = np.swapaxes(data_pca,0,1)

print(data_pca.shape[:])


y = np.zeros(data_pca.shape[0])
y = np.int64(y)
print("y shape : {} ".format(y.shape))


n_neighbors =10

knn = joblib.load('./model/knn')
pca = joblib.load('./model/pca')

acc_knn = knn.score(pca.transform(data_pca), y)
print("KNN (k={})\nTest accuracy = {:.2f}".format(n_neighbors, acc_knn))

print(data_pca.shape[:])
# print(knn.predict(pca.transform(data_pca[0:1 ,:]  )))

for i  in range(data_pca.shape[0]):
    print(knn.predict(pca.transform(data_pca[i : i+1 ,:])))