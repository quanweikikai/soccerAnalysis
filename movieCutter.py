######################################################################################################
## -------------------------------------------movieCutter.py------------------------------------------------------
##
## TODO movieCUtter is a tool that can cut the robosim 2d csv data into several pieces
## TODO the end of the movie piece is determined by judging if  all player's speed are zero or not
##
## TODO get_data read csv file as np.matrix
## TODO getPosSpdMat change the soccer data matrix into a timeList matrix described as below.
##
##      one row shows all the players' position in the reffering moment
##      eg.  time   playerNo.
##            n       player1.x, player1.y, player2.x, player2.y ...
##            n+1     player1.x, player1.y, player2.x, player2.y ...
##            ...     ...
##
## TODO showZeroLine show the index of row which all item in it are zeros
##
## made by Ken in     2015 May 1th
## recent modified in 2015 May 4th
######################################################################################################


#! /usr/bin/python
import numpy as np
import pandas as pd
import os
import pickle

def get_data(path="posSpd.csv"):
	input_data=pd.read_csv(path)
	dataArr=input_data.as_matrix()
	
	return dataArr

def getPosSpdMat(path="posSpd.csv"):
	dataArr=get_data(path)
	
	#draw and make pos spd mat
	length=dataArr.shape[0]
	length=length/46*46

	posIndex=range(0,length,2)
	spdIndex=range(1,length,2)

	playerPosIdx=[i for i in posIndex if not i%46==0]
	playerSpdIdx=[j for j in spdIndex if not j%46==1]
	ballPosIdx=[l for l in posIndex if l%46==0]
	ballSpdIdx=[k for k in spdIndex if k%46==1]

	length_=dataArr[playerPosIdx].shape[0]

	playerPosMat=dataArr[playerPosIdx].reshape(length_/22,44)
	playerSpdMat=dataArr[playerSpdIdx].reshape(length_/22,44)
	ballSpdMat=dataArr[ballSpdIdx]
	ballPosMat=dataArr[ballPosIdx]

	return playerPosMat,playerSpdMat,ballPosMat,ballSpdMat

def showZeroLine(dataArr):
	zeroLineIdx=[]
	
	#length=dataArr.shape[0]
	#dataArr=dataArr.reshape(length/2,44)

	for i in range(dataArr.shape[0]):
		switch=True
		for j in range(dataArr.shape[1]):
			if not dataArr[i,j]==0:
				switch=False
		if switch:
			zeroLineIdx.append(i)

	return zeroLineIdx

workDir=os.getcwd()
def checkSave(dirPath=workDir+"/soccerMatrixData/"):
	prefixName="soccerData"
	index=0
	postfixName=".pkl"
	while os.path.exists(dirPath+prefixName+str(index)+postfixName):
		index+=1

	return dirPath+prefixName+str(index)+postfixName


def cutAndSave(filePath="posSpd.csv",savePath=workDir+"/soccerMatrixData/"):
	playerPosMat,playerSpdMat,ballPosMat,ballSpdMat=getPosSpdMat(filePath)

	#get the cutting points
	zeroIndex=showZeroLine(ballSpdMat)
	cuttingPoint=[]

	for i in range(len(zeroIndex)-1):
		if zeroIndex[i+1]-zeroIndex[i]>20:
			cuttingPoint.append([zeroIndex[i],zeroIndex[i+1]])

	for point in cuttingPoint:
		#length of movie piece must be longer than 100 frame
		if point[1]-point[0]>150:
			
			#save the cutted movie pieces
			filename=checkSave(savePath)
			f=open(filename,"wb")
			dict2Dump={"filename":filePath,"playerPos":playerPosMat[point[0]:point[1]],"ballPos":ballPosMat[point[0]:point[1]],"start":point[0],"end":point[1]}

			pickle.dump(dict2Dump,f)



