#! /usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.signal as sig
from sklearn.decomposition import PCA
from sklearn.cluster import MeanShift,estimate_bandwidth
import matplotlib.animation as animation
from dataReader import reader
import pickle	

markerStyleList=[".","o","v","^","1","8","s","+","*","D","p"]

def get_data(path):
	input_data=pd.read_csv(path)
	dataArr=input_data.as_matrix()
	
	return dataArr

def genData(data,startFrame=0,endFrame=3279):
	#make 2 lists for plot       #plt.plot(list1,list2,"ro")

	#change the input matrix into timeList matrix
	data=data[startFrame*23:endFrame*23]
	length=data.shape[0]
	print "len",length
	data_x=np.zeros((23,length/23))
	data_y=np.zeros((23,length/23))
	print data_x.shape

	for i in range(length/23*23):
		data_x[i%23,i/23]=data[i,0]
		data_y[i%23,i/23]=data[i,1]
			
	return data_x,data_y

def genCuttedData(ballMat,playerMat):
	#this one generate the data for ploting in soccerMatrixData folder
	
	#get the col of playerMat
	
	rows,cols=playerMat.shape

	x_colList=range(0,cols,2)
	y_colList=range(1,cols,2)

	#combine the ball and player position data
	data_x=np.append(ballMat[:,0].reshape(rows,1),playerMat[:,x_colList],axis=1)
	data_y=np.append(ballMat[:,1].reshape(rows,1),playerMat[:,y_colList],axis=1)

	return data_x.T,data_y.T

def updateDot(num,data_x,data_y,plotDot_ball,plotDot_r,plotDot_l):
	plotDot_ball.set_data(data_x[:1,num],data_y[:1,num])
	plotDot_r.set_data(data_x[1:12,num],data_y[1:12,num])
	plotDot_l.set_data(data_x[12:,num],data_y[12:,num])
	print num
	return plotDot_ball,plotDot_r,plotDot_l

def updateDot_(num,data_x,data_y,plotDot_ball,plotDot_r,plotDot_l):
	
	plotDot_ball.set_data(data_x[:1,num],data_y[:1,num])
	for i in range(len(plotDot_r)):
		plotDot_r[i].set_data(data_x[i+1,num],data_y[i+1,num])
		plotDot_l[i].set_data(data_x[i+12,num],data_y[i+12,num])
	print num
	return plotDot_ball,plotDot_r,plotDot_l

def animation_clustering(fps=120,startFrame=0,endFrame=3279,filename="data_.csv"):
	dataset=get_data(filename)
	text="soccer data"
	data_x,data_y=genData(dataset,startFrame,endFrame)
	length=endFrame-startFrame
	text="soccer data"
	fig=plt.figure()
    #initial the plot of ball right team and left team	
	plt.plot([-52.5,52.5,52.5,-52.5,-52.5],[-34,-34,34,34,-34],color="black",linewidth=2.0,linestyle="-")
	plt.plot([0,0],[-34,34],color="black",linewidth=2.0,linestyle="-")
	dot_ball=plt.plot(data_x[:1,0],data_y[:1,0],"ro",markersize=10.0)[0]
	dot_l,dot_r=[],[]
	for ii in range(0,11):
		dot_r.append(plt.plot(data_x[ii+1,0],data_y[ii+1,0],marker=markerStyleList[ii],color="b",label=str(ii),ms=7)[0])
		dot_l.append(plt.plot(data_x[ii+12:,0],data_y[ii+12:,0],marker=markerStyleList[ii],color="g",label=str(ii+11),ms=7)[0])

	plt.xlim([-53,67])
	plt.ylim([-35,35])
	plt.legend(loc='best')
	
	
	#ax.set_title('3D simulation \n '+text)

	stick_ani=animation.FuncAnimation(fig,updateDot_,length,fargs=(data_x,data_y,dot_ball,dot_r,dot_l),interval=fps,blit=False)
	
	#save the plot animation as an mp4 file
	#stick_ani.save("movie1.mp4")
	plt.show()

def aniMov(fileNum,fps=80):
	filename="/home/ken/python_project/soccer/dataMaker/soccerMatrixData/soccerData"+str(fileNum)+".pkl"
	#filename="/home/ken/python_project/soccer/dataMaker/rcgFile/test/soccerMatrixData/soccerData"+str(fileNum)+".pkl"
	f=open(filename,"rb")
	dic=pickle.load(f)
	ballMat=dic["ballPos"]
	playerMat=dic["playerPos"]

	text="soccer data"
	data_x,data_y=genCuttedData(ballMat,playerMat)
	length=data_x.shape[1]

	text="soccer data"
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

	stick_ani=animation.FuncAnimation(fig,updateDot,length,fargs=(data_x,data_y,dot_ball,dot_r,dot_l),interval=fps,blit=False)
	
	#save the plot animation as an mp4 file
	#stick_ani.save("movie1.mp4")
	plt.show()
