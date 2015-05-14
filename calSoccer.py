#!/usr/bin/python

import numpy as np
from makeMatrix import *
import os
import pickle
from ZTrans import *

def calResidual(predictArr,predictedArr):
	'''
	this func calculate the residual
	the predictedArr and predictArr must have the same number of rows'''
	
	#print np.linalg.matrix_rank(predictArr)

	result=np.linalg.lstsq(predictArr,predictedArr)
	#attention!! result[1] is np.ndarray or empty!!
	if result[1].size==0:
		resultErr=0
	else:
		resultErr=result[1][0]

	return result[0],resultErr

def calCau(lag,indexList,playerPos):
	'''minLen-> the minium length of dataList for calculation'''
	#resultList to store the results
	resultListErr_x=[]
	resultListErr_y=[]
	resultListCoefficient_x=[]
	resultListCoefficient_y=[]
	#turn playerPosMat into List
	playerPos=playerPos.tolist()
	for i in range(len(playerPos[0])/2):
		onePlayerErr_x=[]
		onePlayerErr_y=[]
		onePlayerCoefficient_x=[]
		onePlayerCoefficient_y=[]
		for  j in range(0,len(playerPos)-120):
		
			predictAgentArr,toPredictAgentArr_x,toPredictAgentArr_y=matrixMakerSelected(playerPos[j:j+120],lag,indexList,i)
			coefficient_x,squareResidual_x=calResidual(predictAgentArr,toPredictAgentArr_x)
			coefficient_y,squareResidual_y=calResidual(predictAgentArr,toPredictAgentArr_y)
			onePlayerErr_x.append(squareResidual_x)
			onePlayerErr_y.append(squareResidual_y)
			onePlayerCoefficient_x.append(coefficient_x)
			onePlayerCoefficient_y.append(coefficient_y)
		resultListErr_x.append(onePlayerErr_x)
		resultListErr_y.append(onePlayerErr_y)
		resultListCoefficient_x.append(onePlayerCoefficient_x)
		resultListCoefficient_y.append(onePlayerCoefficient_y)
		
		
	#workDir=os.getcwd()+"/soccerMatrixData/"
	#output1=open(workDir+"resultList.pkl","wb")
	#output2=open(workDir+"resultList_coefficient.pkl","wb")
	#pickle.dump(resultList,output1)
	#pickle.dump(resultListCoefficient,output2)

	return resultListErr_x,resultListErr_y,resultListCoefficient_x,resultListCoefficient_y


def zTranPoint(coArr,winLen,lag=1,index=[0,3]):
	
	'''this func transfer a coArr to sample list  *Attention!! this can only change one Arr into Z Trans sample!
	   the zTransform func need input into the type of:
	   [[player1CoList_x,player1CoList_y],[player2CoList_x,player2CoList_y],...]
	   so this func turns a 1 dimension arr into the type of the input in ZTransform
		   '''
	#num of participants
	numOfP=coArr.shape[0]/winLen/2
	#par List
	parList_x=[]
	parList_y=[]
	for i in range(numOfP):
		tmp_x=np.zeros(winLen)
		tmp_y=np.zeros(winLen)
		for j in range(winLen):
			tmp_x[j]=coArr[numOfP*j*2+i*2]
			tmp_y[j]=coArr[numOfP*j*2+i*2+1]
		parList_x.append(tmp_x)
		parList_y.append(tmp_y)

	zClass_x=zTransform(parList_x,lag,index)
	zClass_y=zTransform(parList_y,lag,index)

	sample_theta=[a*np.pi/4 for a in range(5)]
	A_list_x,theta_list_x=zClass_x.getSample(sample_theta)
	A_list_y,theta_list_y=zClass_y.getSample(sample_theta)
	return A_list_x,theta_list_x[1:-1],A_list_y,theta_list_y[1:-1]


workDir=os.getcwd()

def getFileList(dirPath=workDir+"/soccerMatrixData/"):
	'''this one get the all the filename in a folder and wrap it into a list'''
	filenameList=[]
	prefixName="soccerData"
	postfixName=".pkl"
	index=0
	while os.path.exists(dirPath+prefixName+str(index)+postfixName):
		filenameList.append(dirPath+prefixName+str(index)+postfixName)
		index+=1

	return filenameList

def iniList(playerNum):
	'''this func makes empty list for all the player
	eg. if the playerNum is 5 the output will be like:
		player1 player2 player3 player4 player5
		[  []     ,[]     ,[]     ,[]     ,[]  ]
		so if some new values are calculated they can soon be added to the accroding item in the list'''
	output=[]
	for i in range(playerNum):
		output.append([])

	return output


def makePointSpace(index=[0,3],fileList=None,playerNum=22,saveDir=workDir+"/dataPoint/datapoint.pkl"):

	if fileList==None:
		fileList=getFileList()
	
	A_x_x,A_x_y,A_y_x,A_y_y=iniList(playerNum),iniList(playerNum),iniList(playerNum),iniList(playerNum)
	theta_x_x,theta_x_y,theta_y_x,theta_y_y=iniList(playerNum),iniList(playerNum),iniList(playerNum),iniList(playerNum)

	for filename in fileList:
		f=open(filename,"rb")
		dic=pickle.load(f)
		playerPos=dic["playerPos"]
		err_x,err_y,coefficient_x,coefficient_y=calCau(1,index,playerPos)
		
		#input the coefficient Arr into ZTransform
		for i in range(len(coefficient_x)):
			onePlayerAList_x_x=[]
			onePlayerAList_x_y=[]
			onePlayerAList_y_x=[]
			onePlayerAList_y_y=[]
			onePlayerthetaList_x_x=[]
			onePlayerthetaList_x_y=[]
			onePlayerthetaList_y_x=[]
			onePlayerthetaList_y_y=[]

			for j in coefficient_x[i]:
				tmp_A_x_x,tmp_theta_x_x,tmp_A_x_y,tmp_theta_x_y=zTranPoint(j,len(index))

				onePlayerAList_x_x.append(tmp_A_x_x)
				onePlayerAList_x_y.append(tmp_A_x_y)
				onePlayerthetaList_x_x.append(tmp_theta_x_x)
				onePlayerthetaList_x_y.append(tmp_theta_x_y)
			for k in coefficient_y[i]:
				tmp_A_y_x,tmp_theta_y_x,tmp_A_y_y,tmp_theta_y_y=zTranPoint(k,len(index))
				onePlayerAList_y_x.append(tmp_A_y_x)
				onePlayerAList_y_y.append(tmp_A_y_y)
				onePlayerthetaList_y_x.append(tmp_theta_y_x)
				onePlayerthetaList_y_y.append(tmp_theta_y_y)

			A_x_x[i].extend(onePlayerAList_x_x)
			A_x_y[i].extend(onePlayerAList_x_y)
			A_y_x[i].extend(onePlayerAList_y_x)
			A_y_y[i].extend(onePlayerAList_y_y)
			theta_x_x[i].extend(onePlayerthetaList_x_x)
			theta_x_y[i].extend(onePlayerthetaList_x_y)
			theta_y_x[i].extend(onePlayerthetaList_y_x)
			theta_y_y[i].extend(onePlayerthetaList_y_y)

			
	file2save=open(saveDir,"wb")
	dataDict={"A_x_x":A_x_x,"A_x_y":A_x_y,"A_y_x":A_y_x,"A_y_y":A_y_y,"theta_x_x":theta_x_x,"theta_x_y":theta_x_y,"theta_y_x":theta_y_x,"theta_y_y":theta_y_y}
	pickle.dump(dataDict,file2save)
	return A_x_x,A_x_y,A_y_x,A_y_y,theta_x_x,theta_x_y,theta_y_x,theta_y_y

	
