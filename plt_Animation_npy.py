# Animation
# https://vimsky.com/zh-tw/examples/detail/python-method-matplotlib.pyplot.pause.html


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


from os import listdir
from os.path import isdir, isfile, join
import numpy as np

window_size = 10240

state = ["normal","error"]
text_color = ["b","r"]
# mypath = "./iis3_txt/N_50"
data_name = "./realdata/needle_50.npy"

data_read = np.load(data_name)



for i in range(data_read.shape[0]//window_size):
    
    # print(data_read.shape[:])
    plt.plot(data_read[i*window_size : (i+1)*window_size , :] ,label='cubic')
    
    plt.title("data{} state:{}".format(i,state[i%2]),color=text_color[i%2])
    # plt.legend()
    
    # plt.plot(data_read[: 1024 ,0], color = 'b')
    # plt.plot(data_read[: 5120 ,1], color = 'g')
    # plt.plot(data_read[: 5120 ,2], color = 'b')
    plt.pause(0.5)
    plt.clf()


plt.show()
