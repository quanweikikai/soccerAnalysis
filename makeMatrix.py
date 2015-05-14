#!/usr/bin/python

import numpy as np

def matrixMaker(dataList,lag,winLen,agentIndex=0,selfIncluding=True):
	'''this fun turn a time list dataList into embeded matrixs
	   
	   lag->  An int value that define the time gap  ###e.g: lag=3, correspoding relation will be as: a[t]<->b[t-3]
	   winLen->  Length of time window
	   agentIndex->  Index of the agent which the model is to predict
	   dataList->  List with the shape of [[],[],[],[]...]'''

	data=[]
	for i in dataList:
		tmpList=[]
		for j in range(len(i)):
			tmpList.append(i[j]-dataList[0][j])
		data.append(tmpList)

	length=len(data) #frame number
	width=len(data[0]) #len of data in one frame
	# make 3 lists to store the data
	toPredictAgent_x=[]
	toPredictAgent_y=[]
	predictAgentList=[]

	#write data to lists
	for i in range(0,length-lag-winLen+1):
		toPredictAgent_x.append(data[i+winLen-1+lag][agentIndex*2])
		toPredictAgent_y.append(data[i+winLen-1+lag][agentIndex*2+1])

		add2PredictAgentList=[]
		if not selfIncluding:
			for j in range(winLen,0,-1):
				add2PredictAgentList.extend(data[i+j][:agentIndex*2]+data[i+j][agentIndex*2+2:])
		else:
			for k in range(winLen,0,-1):
				add2PredictAgentList.extend(data[i+k])
		predictAgentList.append(add2PredictAgentList)

	predictAgentArr=np.array(predictAgentList)
	toPredictAgentArr_x=np.array(toPredictAgent_x).T
	toPredictAgentArr_y=np.array(toPredictAgent_y).T

	return predictAgentArr,toPredictAgentArr_x,toPredictAgentArr_y

def matrixMakerSelected(dataList,lag,embededIdxList=[0,3],agentIndex=0,selfIncluding=True):
	'''this fun turn a time list dataList into embeded matrix given the selected list
	   
	   lag->  An int value that define the time gap  ###e.g: lag=3, correspoding relation will be as: a[t]<->b[t-3]
	   
	   embededIdxList-> selected Index of the embeded List
	   eg. the default one [0,3] means: (lag=1)
	   predicted t    [-------------------------]
	   predict   t-1  [-------------------------] *selected
	   predict   t-2  [-------------------------]
	   predict   t-3  [-------------------------]
	   predict   t-4  [-------------------------] *selected
	   the selected one choose only the t-1 and t-4 row to predict the "t" one

	   agentIndex->  Index of the agent which the model is to predict
	   
	   dataList->  List with the shape of [[],[],[],[]...]'''


	data=[]
	for i in dataList:
		tmpList=[]
		for j in range(len(i)):
			tmpList.append(i[j]-dataList[0][j])
		data.append(tmpList)

	length=len(data) #frame number
	width=len(data[0]) #len of data in one frame
	# make 3 lists to store the data
	toPredictAgent_x=[]
	toPredictAgent_y=[]
	predictAgentList=[]

	#write data to lists
	for i in range(0,length-lag-embededIdxList[0]):
		toPredictAgent_x.append(data[i+embededIdxList[0]+lag][agentIndex*2])
		toPredictAgent_y.append(data[i+embededIdxList[0]+lag][agentIndex*2+1])

		add2PredictAgentList=[]
		if not selfIncluding:
			for j in range(-1,-len(embededIdxList)-1,-1):
				add2PredictAgentList.extend(data[i+embededIdxList[j]][:agentIndex*2]+data[i+j][agentIndex*2+2:])
		else:
			for k in range(-1,-len(embededIdxList)-1,-1):
				add2PredictAgentList.extend(data[i+k])
		predictAgentList.append(add2PredictAgentList)

	predictAgentArr=np.array(predictAgentList)
	toPredictAgentArr_x=np.array(toPredictAgent_x).T
	toPredictAgentArr_y=np.array(toPredictAgent_y).T

	del(embededIdxList)

	return predictAgentArr,toPredictAgentArr_x,toPredictAgentArr_y
