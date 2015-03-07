#!/usr/bin/python

import numpy as np

def matrixMaker(dataList,agentIndex=0):
	'''this fun turn a time list dataList into embeded matrixsi
	   lag is an int value that define the time gap
	   winLen is the length of time window
	   agentIndex is the index of the agent which the model is to predict'''

	length=len(dataList)
	width=len(dataList[0])
	toPredictAgent_x=[]
	toPredictAgent_y=[]
	preditAgentList=[]

