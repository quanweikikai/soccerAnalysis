#!/usr/bin/python

import numpy as np

def matrixMaker(dataList,lag,winLen,agentIndex=0):
	'''this fun turn a time list dataList into embeded matrixsi
	   
	   lag->  An int value that define the time gap  ###e.g: lag=3, correspoding relation will be as: a[t]<->b[t-3]
	   winLen->  Length of time window
	   agentIndex->  Index of the agent which the model is to predict
	   dataList->  List with the shape of [[],[],[],[]...]'''

	length=len(dataList) #frame number
	width=len(dataList[0]) #len of data in one frame
	# make 3 lists to store the data
	toPredictAgent_x=[]
	toPredictAgent_y=[]
	predictAgentList=[]

	#write data to lists
	for i in range(0,length-lag-winLen+1):
		toPredictAgent_x.append(dataList[i+winLen-1+lag][agentIndex*2])
		toPredictAgent_y.append(dataList[i+winLen-1+lag][agentIndex*2+1])

		add2PredictAgentList=[]
		for j in range(winLen):
			add2PredictAgentList.extend(dataList[i+j][:agentIndex*2]+dataList[i+j][agentIndex*2+2:])
		predictAgentList.append(add2PredictAgentList)

	predictAgentArr=np.array(predictAgentList)
	toPredictAgentArr_x=np.array(toPredictAgent_x).T
	toPredictAgentArr_y=np.array(toPredictAgent_y).T

	return predictAgentArr,toPredictAgentArr_x,toPredictAgentArr_y


