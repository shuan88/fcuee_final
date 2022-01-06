from tds import * 
import joblib


# data0_name = "realdata/iis3_N_50.npy"
# data1_name = "realdata/iis3_N_100.npy"


# data0_name = "../Data_120_nor/N/2021-08-03_N_S100_L0_Acc8_BW184_1050Hz_0.npy"
# data1_name = "../Data_120_nor/RU/2021-08-04_RU_S100_L100_Acc8_BW184_1050Hz_0.npy"
# data2_name = "../Data_120_nor/N/stm32_2021-07-23_N_S25_L50_Acc8_BW184_Q540_1_1055Hz_2.npy"

# data0_name = "realdata/needle_100.npy"
# data1_name = "realdata/needle_50.npy"
# data2_name = "realdata/needle_error.npy"

data0_name = "../iis3_SerialRead/L100.npy"
data1_name = "../iis3_SerialRead/L50.npy"
data2_name = "../iis3_SerialRead/L0.npy"

window_size = 1024


# data_lable_0 = np.swapaxes(TDS7_feature(data0_name,1024)[:,:,0],0,1)
# data_lable_1 = np.swapaxes(TDS7_feature(data1_name,1024)[:,:,0],0,1)
# data_lable_2 = np.swapaxes(TDS7_feature(data2_name,1024)[:,:,0],0,1)


data_lable_0 = TDS7_feature(data0_name,window_size)
data_lable_1 = TDS7_feature(data1_name,window_size)
data_lable_2 = TDS7_feature(data2_name,window_size)


data_lable_0 = np.vstack([data_lable_0[:,:,0],data_lable_0[:,:,1],data_lable_0[:,:,2]])
data_lable_1 = np.vstack([data_lable_1[:,:,0],data_lable_1[:,:,1],data_lable_1[:,:,2]])
data_lable_2 = np.vstack([data_lable_2[:,:,0],data_lable_2[:,:,1],data_lable_2[:,:,2]])


# print(data_lable_0.shape[:])
# print(data_lable_1.shape[:])
# print(data_lable_2.shape[:])

# y_lable = np.append (np.zeros( data_lable_0.shape[0] ) , np.ones( data_lable_1.shape[0] ))
# data_pca = np.append(data_lable_0,data_lable_1,axis=0)

data_pca = np.append(data_lable_0,data_lable_1,axis=1)
data_pca = np.append(data_pca,data_lable_2,axis=1)

data_pca = np.swapaxes(data_pca,0,1)
print(data_pca.shape[:])
## 2400 , 24

y = np.append (np.zeros(data_lable_0.shape[-1]) , np.ones(data_lable_1.shape[-1]))
y = np.append (y , np.ones(data_lable_2.shape[-1])*2)
y = np.int64(y)

print("y shape : {} ".format(y.shape))

## (data len , feature * axis )

################################################################
##################### model ####################################
################################################################
n_neighbors = 10
random_state = 0
n_components = 3

h = 0.02  # step size in the mesh

## Split into train/test 
## https://iter01.com/522027.html
# X_train, X_test, y_train, y_test = train_test_split(data_pca, y, test_size=0.3, stratify=y, random_state=random_state)

X_train, X_test, y_train, y_test = train_test_split(data_pca, y, test_size=0.3)

print(X_train.shape , X_test.shape)
print(y_train.shape , y_test.shape)

pca = make_pipeline(StandardScaler(), PCA(n_components=n_components, random_state=random_state))

# Use a nearest neighbor classifier to evaluate the methods
knn = KNeighborsClassifier(n_neighbors=n_neighbors , weights ='distance')

pca.fit(X_train, y_train)

# Fit a nearest neighbor classifier on the embedded training set
knn.fit(pca.transform(X_train), y_train)

# Compute the nearest neighbor accuracy on the embedded test set
acc_knn = knn.score(pca.transform(X_test), y_test)
print("KNN (k={})\nTest accuracy = {:.2f}".format(n_neighbors, acc_knn))

# Embed the data set in 2 dimensions using the fitted model
X_embedded = pca.transform(data_pca)


joblib.dump(knn, './model/knn_{}'.format(window_size))
joblib.dump(pca, './model/pca_{}'.format(window_size))


################################################################
###### Plot the results ########################################
################################################################


plt.figure(figsize=(8, 6))

if n_components < 3: 
    x_min, x_max = X_embedded[:, 0].min() - 1, X_embedded[:, 0].max() + 1
    y_min, y_max = X_embedded[:, 1].min() - 1, X_embedded[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    cmap_light = ListedColormap(["orange", "cyan", "cornflowerblue"])
    cmap_bold = ["darkorange", "c", "darkblue"]
    plt.contourf(xx, yy, Z, cmap=cmap_light)


plt.scatter(X_embedded[:, 0], X_embedded[:, 1], c=y, s=30, cmap="Set1")
plt.title("KNN (k={})\nTest accuracy = {:.2f}".format(n_neighbors, acc_knn))
plt.show()


# ## 3D plot
if n_components >= 3: 
    fig = plt.figure(1, figsize=(12, 9))
    plt.clf()
    ax = Axes3D(fig, rect=[0, 0, 0.95, 1], elev=48, azim=134)
    # y = np.choose(y, [1, 2, 0]).astype(float)
    y = np.choose(y, [2,4,0]).astype(float)
    ax.scatter(X_embedded[:, 0], X_embedded[:, 1],X_embedded[:, 2]  , c=y , cmap=plt.cm.nipy_spectral, edgecolor="k")
    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.legend()
    plt.show()