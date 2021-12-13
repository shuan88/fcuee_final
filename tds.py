from os import listdir
from os.path import isdir, isfile, join
from scipy import signal
from mpl_toolkits.mplot3d import Axes3D

from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier, NeighborhoodComponentsAnalysis

from matplotlib.colors import ListedColormap

# from numba import jit
# from numba import vectorize

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import seaborn as sns
import os, sys, shutil
import scipy

# import tensorflow as tf


def data_process_reshape(data, point=1024):
    data = data.reshape(-1,point,data.shape[-1])
    return data

def plot3axis (data , name = "NULL" , save_fig = False ,save_dir = "."):
    plt.figure(figsize=(20,5))
    plt.plot(data)
    if name != "NULL":
        plt.title(name)
        if save_fig == True:
            plt.savefig('{}/{}.png'.format(save_dir,name))
    plt.show()
    
def Normalized(data , scaler = True):
    # print(np.max(data),np.min(data))
    scaler = MinMaxScaler()
    scaler.fit(data)
    return scaler.transform(data)

def Normalized_SKW(data , scaler = True):
    scaler = MinMaxScaler(feature_range=(-1,1))
    scaler.fit(data)
    return scaler.transform(data)

def RMS(data):
    return np.array(np.sqrt(np.mean(data**2, axis=1)))
def VAR(data):
    return np.var(data, axis=1)
def KUR(data ,fisher=True):
    return scipy.stats.kurtosis(data, axis =1, fisher=True)
def SKW(data):
    return scipy.stats.skew(data, axis=1)
    
def TDS7_feature(name,sample_rate=1000):
    data = np.load(name)
    scaler = MinMaxScaler(feature_range=(-16,16))
    scaler.fit(data)
    data = scaler.transform(data)
    data_second = data_process_reshape(data,sample_rate)
    # data_second = data_process_reshape(np.load(name),sample_rate)
    
    data_RMS = (RMS(data_second))
    data_VAR = (VAR(data_second) )
    data_KUR = (KUR(data_second) )
    data_PV = ((np.max(data_second,axis=1)-np.min(data_second,axis=1))/2 )
    data_SKW =(SKW(data_second))
    data_MED =(np.median(data_second,axis=1))
    
    # print(data_second.shape[:])
    # # ## Root Mean Value
    # data_RMS = Normalized(RMS(data_second))
    # data_VAR = Normalized(VAR(data_second) )
    # data_KUR = Normalized(KUR(data_second) )
    # data_PV = Normalized((np.max(data_second,axis=1)-np.min(data_second,axis=1))/2 )
    # data_SKW =Normalized_SKW(SKW(data_second))
    # data_MED =Normalized(np.median(data_second,axis=1))
    # return np.stack((data_RMS,data_VAR,data_KUR,data_PV,data_SKW,data_MED))
    return np.stack((data_RMS,data_VAR,data_KUR,data_PV,
                    data_SKW,data_MED,np.multiply(data_RMS,data_KUR),
                    np.multiply(data_RMS,data_PV) ))

def TDS7_feature_realtime(data,sample_rate=1000):
    scaler = MinMaxScaler(feature_range=(-16,16))
    scaler.fit(data)
    data = scaler.transform(data)
    data_second = data_process_reshape(data,sample_rate)
    # print(data_second.shape[:])
    
    data_RMS = (RMS(data_second))
    data_VAR = (VAR(data_second) )
    data_KUR = (KUR(data_second) )
    data_PV = ((np.max(data_second,axis=1)-np.min(data_second,axis=1))/2 )
    data_SKW =(SKW(data_second))
    data_MED =(np.median(data_second,axis=1))
    # return np.stack((data_RMS,data_VAR,data_KUR,data_PV,data_SKW,data_MED))
    return np.stack((data_RMS,data_VAR,data_KUR,data_PV,
                    data_SKW,data_MED,np.multiply(data_RMS,data_KUR),
                    np.multiply(data_RMS,data_PV) ))
    
    
