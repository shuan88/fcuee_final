import serial 
import numpy as np
import os, sys
import matplotlib.pyplot as plt



quantity = 20
path = "../iis3_SerialRead/L100"
load_data = np.load("../iis3_SerialRead/{}/data0.npy".format(path))
print(load_data.shape)
# print(load_data)
for i in range (1, quantity):
    data_read = np.load("../iis3_SerialRead/{}/data{}.npy".format(path,i))
    print(data_read.shape)
    # data_read = np.load("./test_3_1/data" + str(i) + ".npy")
    load_data = np.vstack([load_data,data_read])

load_data = load_data[: quantity*10240 , :]
print(load_data.shape)

data_name = "../iis3_SerialRead/L100.npy"
np.save(data_name,load_data)


