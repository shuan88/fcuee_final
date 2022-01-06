import serial 
import time
import datetime
# import pymongo
# import json
import numpy as np
# import pandas as pd 
import os, sys
import matplotlib.pyplot as plt


""" linkit 
    ser = pyserial.Serial('/dev/tty.usbmodem14201',500000) 
"""

# COM_PORT = '/dev/tty.usbmodem14101'    # port name
# COM_PORT = '/dev/tty.usbmodem14203'    # port name
# COM_PORT = '/dev/tty.usbmodem1414403'    # port name 
COM_PORT = '/dev/cu.usbserial-0001'    # port name
# COM_PORT = 'COM5' # for windows USE "COM[number]"

BAUD_RATES = 250000    # SET BAUD_RATES 115200,250000,500000,1000000
# BAUD_RATES = 500000    # SET BAUD_RATES 115200,250000,500000,1000000
# BAUD_RATES = 115200    # SET BAUD_RATES 115200,250000,500000,1000000
ser = serial.Serial(COM_PORT, BAUD_RATES)   # init Serial settings

quantity = 2  # How many k data you want `60` is about 10 min  
data_size = 1024 # How many data size per saved file Recomand use 10000

# path = "{}_N_S50_L0" .format(datetime.date.today())
# path = "{}_L100" .format(datetime.date.today())
path = "L500"
""" 命名方式
    N：狀態，總共有四種(N=>正常馬達、RU=>轉子不平衡、RB=>轉子斷條、SS=>定子短路)
    S{}：速度與運轉功率=>S：speed，25：運轉%數(0,25,50,75,100)
    L{}：附載 : 0,25,50,75,100,125
    f{}：Sample rate (Hz)
"""
    

IncommingNum = ser.readline()
i = 0

if os.path.isdir("../iis3_SerialRead/{}".format(path)):
    path_temp = path
    while os.path.isdir("../iis3_SerialRead/{}".format(path_temp)):
        i+=1
        path_temp = str(path+ "_"+str(i))
        print(path_temp)
    path = path_temp
os.mkdir("../iis3_SerialRead/{}".format(path))

final_frequency = 0


# time0 = int(datetime.datetime.utcnow().timestamp())
time0 = int(time.time())

time.sleep(10)
print ("Start")

for i in range(quantity):
    # time1 = int(datetime.datetime.utcnow().timestamp())
    new_array = np.zeros((data_size,3))
    time1 = int(time.time())
    # new_array = np.fromstring(ser.readline().decode('utf-8'), dtype=float, sep=',')
    counter = 0
    while counter < data_size:
        IncommingNum = ser.readline()
        data = np.fromstring(IncommingNum.decode('utf-8'), dtype=float, sep=',')
        # print(data)
        if data.shape[0] == 3 :
            new_array[counter,:] = data
            # new_array = np.append(new_array,data)
            counter += 1
        else :
            print(counter)
    """
    for counter in range(data_size - 1):
        IncommingNum = ser.readline()
        # data = IncommingNum.decode('utf-8')   # UTF-8 decoder
        data = np.fromstring(IncommingNum.decode('utf-8'), dtype=float, sep=',')
        try:
            if data.shape[0] ==3 :
                # print(data) 
                # print(counter," ",data)
                new_array = np.append(new_array,data)
            else :
                print(counter)
                counter -= 1
                print("{}noooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo".format(counter))
        except:
            print("errorrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
            continue
    """
    
    # data_time = (datetime.datetime.utcnow().timestamp()- time1)
    data_time = (time.time() - time1)
    frequency = np.int16(data_size/data_time)
    final_frequency += frequency
    # arr_size = np.int16((new_array.shape[0])/3)
    
    # np.save("./{}/data{}".format(path,i), (np.reshape(new_array, (arr_size,3))))
    # np.save("../iis3_SerialRead/{}/data{}".format(path,i), (np.reshape(new_array, (-1,3))))
    np.save("../iis3_SerialRead/{}/data{}".format(path,i),new_array)
    # pd.DataFrame(new_array).to_csv("./file_org.csv")
    print("time cost :" ,  str(data_time) ) # show time cost
    # print(arr_size)
    print(i,"> ","f = " ,str(frequency),"Hz" )
    # del new_array
    

# print((datetime.datetime.utcnow().timestamp() - time0))
# final_frequency = (quantity * data_size)/(datetime.datetime.utcnow().timestamp() - time0)
# final_frequency = (quantity * data_size)/(time.time() - time0)
final_frequency = final_frequency / quantity
print("avg f = {}".format(final_frequency))

# load_data = np.load("./{}/data0.npy".format(path))
load_data = np.load("../iis3_SerialRead/{}/data0.npy".format(path))
print(load_data)
for i in range (1, quantity-1):
    data_read = np.load("../iis3_SerialRead/{}/data{}.npy".format(path,i))
    # data_read = np.load("./test_3_1/data" + str(i) + ".npy")
    load_data = np.vstack([load_data,data_read])

np.save("../iis3_SerialRead/{}_{}Hz".format(path,frequency),load_data)
# load_data[:,1] += 0.4881932
# load_data[:,2] += 10.27560595


N = len(load_data) 
F = final_frequency
freq = np.fft.rfftfreq(N,d=F**-1)
for i in range(3):
    plt.subplot(3, 3, i+1)
    sp = np.fft.rfft(load_data[:,i])
    # sp = np.fft.rfft(load_data[:,i],norm="forward")
    ymax = np.argmax(sp)
    # print(sp.shape[:])
    print ("data {} max:{}".format(i,ymax))
    # plt.plot( freq , np.abs(sp))
    plt.plot( freq[1:-1] , np.abs(sp[1:-1]))
    plt.subplot(3, 3, i+4)
    plt.plot( load_data[:,i])
    plt.subplot(3, 3, i+7)
    plt.plot( load_data[0:100,i])

# plt.savefig("../iis3_SerialRead/{}_{}Hz.png".format(path,frequency))
plt.show()


