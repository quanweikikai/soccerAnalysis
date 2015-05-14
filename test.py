#! /usr/bin/python

################################################################################
#-------------------------------test.py-----------------------------------------
# TODO this py file change the test rcg files into data point for testing
# TODO 1.change the rcg file to np.matrix (np.ndarray)
# TODO 2.use the granger causality to calculate the coefficient dataArr
# TODO 3.use the z transform to change the dataArr to spectral sample list
# TODO 4.draw the saved kMeans class and classify the sample data
# TODO 5.count the sample label and generate the bag of words data
# TODO 6.dump the result into SVM and classify the player
# para saveDir_: dirpath that save the cutted movie data pkl file and datapoint data
# para filepath: dirpath that save the pca and KMeans class 
#
# author: Ken made in 2015.05.13
# latest modified:2015.05.13
################################################################################

import pickle
import os
from movieCutter import *
from main import *
from calSoccer import *
import sklearn.cluster.k_means_ as km


currentDir=os.getcwd()
def test(k,nComponents,filepath=currentDir+"/rcgFile/csvFile/"):
	saveDir_=currentDir+"/rcgFile/test/soccerMatrixData/"
	
	#cut and save all the movie pieces
	cut_save_all(filepath,saveDir_)
	
	filenameList=getFileList(saveDir_)
	# dataPointPath -> place to save the dataPoint (pkl file)
	dataPointPath=currentDir+"/rcgFile/test/datapoint/dataPoint.pkl"
	c1,c2,c3,c4,c5,c6,c7,c8=makePointSpace(fileList=filenameList,saveDir=dataPointPath)
	#read data
	f=open(dataPointPath,"rb")
	#data dict
	dataDic=pickle.load(f)
	#get all keys in data point dict
	key=dataDic.keys()

	#from here read the saved kmeans and pca class to transform data

	#path that pca and kmeans file in 
	filepath=currentDir+"/dataPoint/pca_"+str(k)+"_"+str(nComponents)+".pkl"
	
	classF=open(filepath,"rb")
	KMclassDic=pickle.load(classF)
	bowPoint=[]
	
	for ii in range(len(key)):
		#get the according keans in KMeansList
		KMclass=KMclassDic["KMeans"][ii]

		oneFeatureValueBowPoint=[]
		#all player data in one kind feature value
		playerData=dataDic[key[ii]]
		setList=range(KMclass.k)
		for jj in playerData:
			labelResult=KMclass.predict(jj)
			labelResultList=labelResult.tolist()
			labelResultListSize=len(labelResultList)
			oneBowPoint=[]
			for ll in setList:
				oneBowPoint.append(labelResultList.count(ll)/float(labelResultListSize))
			oneFeatureValueBowPoint.append(oneBowPoint)
		bowPoint.append(oneFeatureValueBowPoint)

	allBowPoint=[]
	#allBowPoint has the shape like:
	# player1            player2           player3
	#[feature value]    [       ]         [       ]
	for mm in range(len(bowPoint[0])):
		tmp_=[]
		for nn in bowPoint:
			tmp_.append(nn[mm])
		allBowPoint.append(tmp_)
	
	#get pca class
	pcaClass=KMclassDic["pca"]
	featureValueList=pcaClass.fit_transform(allBowPoint)

	#save the test feature Value
	featureValueSavePath=currentDir+"/rcgFile/test/datapoint/featurePoint.pkl"
	saveFile=open(featureValueSavePath,"wb")
	pickle.dump(featureValueList,saveFile)

	return featureValueList

	

