from tds import * 
import joblib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial 

BAUD_RATES = 250000    # SET BAUD_RATES 115200,250000,500000,1000000
COM_PORT = '/dev/cu.usbserial-0001'    # port name
ser = serial.Serial(COM_PORT, BAUD_RATES)   # init Serial settings
IncommingNum = ser.readline()


state = ["normal","low" ,"error"]
text_color = ["b","g","r"]
marker_style = ["o","^","x"]
window_size = 1024


pca = joblib.load('./model/pca_1024')
knn = joblib.load('./model/knn_1024')



x_label = 0
while True:
    # for i in range(window_size):
    new_array = np.zeros((window_size,3))
    # new_array = np.fromstring(ser.readline().decode('utf-8'), dtype=float, sep=',')
    counter = 0
    while counter < window_size:
        IncommingNum = ser.readline()
        data = np.fromstring(IncommingNum.decode('utf-8'), dtype=float, sep=',')
        if data.shape[0] == 3 :
            new_array[counter,:] = data
            counter += 1
        else :
            print(counter)
    data_lable_0 = TDS7_feature_realtime(new_array,window_size)
    # print(data_lable_0.shape)
    print(data_lable_0)
    data_pca = np.vstack([data_lable_0[:,:,0],
                    data_lable_0[:,:,1],
                        data_lable_0[:,:,2]])
    data_pca = np.swapaxes(data_pca,0,1)
    result = knn.predict(pca.transform(data_pca))[0]
    # print(result)
    plt.plot(new_array)
    # plt.scatter(x_label,data_lable_0[0,x_label,0] , color=text_color[result] , vmin=0, vmax=1 ,marker = marker_style[result])
    plt.title("data{} state:{}".format(x_label,state[result]),color=text_color[result])
    x_label += 1
    plt.pause(0.1)
    plt.clf()
plt.show()
        