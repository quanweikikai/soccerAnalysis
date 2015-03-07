#! /usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.signal as sig
from sklearn.decomposition import PCA
from sklearn.cluster import MeanShift,estimate_bandwidth
import matplotlib.animation as animation
from dataReader import reader

def get_data(path):
	input_data=pd.read_csv(path)
	dataArr=input_data.as_matrix()
	
	return dataArr

def genData(data):
	#make 2 lists for plot       #plt.plot(list1,list2,"ro")
	length=data.shape[0]
	print "len",length
	data_x=np.zeros((23,length/23))
	data_y=np.zeros((23,length/23))
	print data_x.shape

	for i in range(length/23*23):
		data_x[i%23,i/23]=data[i,0]
		data_y[i%23,i/23]=data[i,1]
			
	return data_x,data_y

def updateDot(num,data_x,data_y,plotDot_ball,plotDot_r,plotDot_l):
	plotDot_ball.set_data(data_x[:1,num],data_y[:1,num])
	plotDot_r.set_data(data_x[1:12,num],data_y[1:12,num])
	plotDot_l.set_data(data_x[12:,num],data_y[12:,num])
	print num
	return plotDot_ball,plotDot_r,plotDot_l

def animation_clustering(filename="data_.csv"):
	dataset=get_data(filename)
	length=dataset.shape[0]
	text="soccer data"
	data_x,data_y=genData(dataset)
	fig=plt.figure()
    #initial the plot of ball right team and left team	
	plt.plot([-52.5,52.5,52.5,-52.5,-52.5],[-34,-34,34,34,-34],color="black",linewidth=2.0,linestyle="-")
	plt.plot([0,0],[-34,34],color="black",linewidth=2.0,linestyle="-")
	dot_ball=plt.plot(data_x[:1,0],data_y[:1,0],"ro",markersize=9.0)[0]
	dot_r=plt.plot(data_x[1:12,0],data_y[1:12,0],"bo")[0]
	dot_l=plt.plot(data_x[12:,0],data_y[12:,0],"go")[0]

	plt.xlim([-53,53])
	plt.ylim([-35,35])
	
	
	#ax.set_title('3D simulation \n '+text)

	stick_ani=animation.FuncAnimation(fig,updateDot,length/23,fargs=(data_x,data_y,dot_ball,dot_r,dot_l),interval=80,blit=False)
	stick_ani.save("movie.mp4")
	plt.show()
