#! /usr/bin/python

from calculateCausality import *
from ZTrans import *
from dataReader import *
import pickle
import numpy as np

def zTranPoint(coArr,winLen,lag=1):
	'''this func transfer a coArr to sample list'''
	#num of participants
	numOfP=coArr.shape[0]/winLen
	#par List
	parList=[]
	for i in range(numOfP):
		tmp=np.zeros(winLen)
		for j in range(winLen):
			tmp[j]=coArr[numOfP*j+i]
		parList.append(tmp)

	zClass=zTransform(parList,lag)
	sample_theta=[a*np.pi/4 for a in range(5)]
	A_list,theta_list=zClass.getSample(sample_theta)
	return A_list,theta_list[1:-1]

def makeFilenameList():
	fList=[]
	for i in range(2):
		fList.append("makeDataRun2P_"+str(i)+".pkl")
	for j in range(2):
		fList.append("makeDataRunParallel"+str(j)+".pkl")
		
	return fList
		

fList=makeFilenameList()

def makePointSpace(filenameList=fList):
	'''this func draw all the data with the type of:
	   one that predict x and y: resultList-> [[[A_list_x],[theta_list_x]],[[A_list_y],[theta_list_y]]]'''
	resultList_x_A=[]
	resultList_y_A=[]
	resultList_x_theta=[]
	resultList_y_theta=[]

	for filename in filenameList:
		residual,coefficient=calAll(300,1,10,0,filename)
		for i in coefficient:
			for j in i:
				A_list_x,theta_list_x=zTranPoint(j[0],10)
				A_list_y,theta_list_y=zTranPoint(j[1],10)
				resultList_x_A.append(A_list_x)
				resultList_y_A.append(A_list_y)
				resultList_x_theta.append(theta_list_x)
				resultList_y_theta.append(theta_list_y)
	#file to write data
	output=open("dataSpace.pkl","wb")
	resultDic={"x_A":resultList_x_A,"y_A":resultList_y_A,"x_theta":resultList_x_theta,"y_theta":resultList_y_theta}
	pickle.dump(resultDic,output)


