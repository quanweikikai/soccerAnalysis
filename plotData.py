#! /usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.signal as sig
from sklearn.decomposition import PCA
from sklearn.cluster import MeanShift,estimate_bandwidth
import matplotlib.animation as animation
from dataReader import reader


def genData(data):
	'''data is a list with the shape of [[],[]...]'''
	#make 2 lists for plot       #plt.plot(list1,list2,"ro")
	length=len(data)
	width=len(data[0])
	print "len",length
	data_x=np.zeros((width/2,length))
	data_y=np.zeros((width/2,length))

	for i in range(length):
		for j in range(width/2):
			data_x[j,i]=data[i][j*2]
			data_y[j,i]=data[i][j*2+1]
			
	return data_x,data_y

def updateDot(num,data_x,data_y,plotDot):
	plotDot.set_data(data_x[:,num],data_y[:,num])
	print num
	return plotDot

def animation_Data(filename='data.pkl'):
	dataList=reader(filename)
	length=len(dataList)
	width=len(dataList[0])
	
	text="data"
	data_x,data_y=genData(dataList)
	fig=plt.figure()
    #initial the plot	
	dot=plt.plot(data_x[:,0],data_y[:,0],"ro")[0]

	plt.xlim([np.min(data_x),np.max(data_x)])
	plt.ylim([np.min(data_y),np.max(data_y)])

	
	#ax.set_title('3D simulation \n '+text)

	stick_ani=animation.FuncAnimation(fig,updateDot,length,fargs=(data_x,data_y,dot),interval=10,blit=False)
	stick_ani.save(filename+".mp4")
	plt.show()

def plotTest(filename):
	#prefix="makeDataRun2P_"
	#postfix=".pkl"
	#filename=prefix+str(index)+postfix
	animation_Data(filename)


	

