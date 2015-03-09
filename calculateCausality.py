#!/usr/bin/python

import numpy as np
from makeMatrix import *
from dataReader import *

def calResidual(predictArr,predictedArr):
	'''
	this func calculate the residual
	the predictedArr and predictArr must have the same number of rows'''

	result=np.linalg.lstsq(predictArr,predictedArr)

	return result[0],result[1][0]

def calAll(minLen,lag,winLen,agentIndex=0,filename="data.pkl"):
	'''minLen-> the minium length of dataList for calculation'''
	dataList=reader(filename)
	#resultList to store the results
	resultList=[]
	for i in range(minLen,len(dataList),(len(dataList)-minLen-1)/20):
		listof1Len=[]
		for j in range(len(dataList)-minLen+1):
			predictAgentArr,toPredictAgentArr_x,toPredictAgentArr_y=matrixMaker(dataList[j:j+i],5,10)
			coefficient_x,squareResidual_x=calResidual(predictAgentArr,toPredictAgentArr_x)
			coefficient_y,squareResidual_y=calResidual(predictAgentArr,toPredictAgentArr_y)
			listof1Len.append([squareResidual_x,squareResidual_y])
		resultList.append(listof1Len)
		print i
	
	output=open("resultList.pkl","wb")
	pickle.dump(resultList,output)
	return resultList

	

