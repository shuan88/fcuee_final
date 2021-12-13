from tds import * 
import joblib
import matplotlib.pyplot as plt
import matplotlib.animation as animation


state = ["normal","low" ,"error"]
text_color = ["b","g","r"]
marker_style = ["o","^","x"]

window_size = 1024


# data0_name = "realdata/needle_muti.npy"
data0_name = "realdata/needle_100.npy"
# data0_name = "realdata/needle_error.npy"
data_read = np.load(data0_name)

data_lable_0 = TDS7_feature(data0_name,window_size)
print(data_lable_0.shape)
data_pca = np.vstack([data_lable_0[:,:,0],
                      data_lable_0[:,:,1],
                      data_lable_0[:,:,2]])
data_pca = np.swapaxes(data_pca,0,1)


print(data_pca.shape[:])


y = np.zeros(data_pca.shape[0])
y = np.int64(y)
print("y shape : {} ".format(y.shape))

n_neighbors =10

knn = joblib.load('./model/knn_1024')
pca = joblib.load('./model/pca_1024')


print(data_pca.shape[:])
# print(knn.predict(pca.transform(data_pca[0:1 ,:]  )))

for i  in range(data_pca.shape[0]):
    result = knn.predict(pca.transform(data_pca[i : i+1 ,:]))[0]
    # plt.plot(data_read[i*window_size : (i+1)*window_size , :] )
    
    plt.scatter(i,data_lable_0[0,i,0] , color=text_color[result] , vmin=0, vmax=1 ,marker = marker_style[result])    
    plt.title("data{} state:{}".format(i,state[result]),color=text_color[result])
    
    
    plt.pause(0.05)
    # plt.clf()
    
# plt.show()