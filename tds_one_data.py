import serial 
import numpy as np
import os, sys
import matplotlib.pyplot as plt
from tds import * 
import joblib

window_size = 1024
quantity = 20

pca = joblib.load('./model/pca_1024')
knn = joblib.load('./model/knn_1024')

# load_data = np.load("../iis3_SerialRead/{}/data2.npy".format(path))


path = "../iis3_SerialRead/L0"
for i in range (1, quantity):
    load_data = np.load("../iis3_SerialRead/{}/data{}.npy".format(path,i))
    load_data = load_data[:window_size ,:]
    
    print(load_data.shape)

    data_lable_0 = TDS7_feature_realtime(load_data,window_size)
    # print(data_lable_0)

    data_pca = np.vstack([data_lable_0[:,:,0],
                    data_lable_0[:,:,1],
                        data_lable_0[:,:,2]])
    data_pca = np.swapaxes(data_pca,0,1)
    result = knn.predict(pca.transform(data_pca))[0]
    print(result)