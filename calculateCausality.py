#!/usr/bin/python

import numpy as np
from makeMatrix import *
from dataReader import *

def calResidual(predictArr,predictedArr):
	'''
	this func calculate the residual
	the predictedArr and predictArr must have the same number of rows'''
	
	#print np.linalg.matrix_rank(predictArr)

	result=np.linalg.lstsq(predictArr,predictedArr)

	return result[0],result[1][0]

def calAll(minLen,lag,winLen,agentIndex=0,filename="data.pkl"):
	'''minLen-> the minium length of dataList for calculation'''
	dataList=reader(filename)
	#resultList to store the results
	resultList=[]
	resultListCoefficient=[]
	for i in range(minLen,len(dataList),(len(dataList)-minLen-1)/20):
		listof1Len=[]
		listof1LenCoefficient=[]
		for j in range(len(dataList)-minLen+1):
			predictAgentArr,toPredictAgentArr_x,toPredictAgentArr_y=matrixMaker(dataList[j:j+i],lag,winLen)
			coefficient_x,squareResidual_x=calResidual(predictAgentArr,toPredictAgentArr_x)
			coefficient_y,squareResidual_y=calResidual(predictAgentArr,toPredictAgentArr_y)
			listof1Len.append([squareResidual_x,squareResidual_y])
			listof1LenCoefficient.append([coefficient_x,coefficient_y])
		resultList.append(listof1Len)
		resultListCoefficient.append(listof1LenCoefficient)
		print i
	
	output=open("resultList.pkl","wb")
	output=open("resultList_coefficient.pkl","wb")
	pickle.dump(resultList,output)
	pickle.dump(resultListCoefficient,output)
	return resultList,resultListCoefficient

	

