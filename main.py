#! /usr/bin/python

import os
from movieCutter import *
from bagOfWords import *
import pickle
from sklearn.decomposition import PCA

currentDir=os.getcwd()

def cut_save_all(filepath=currentDir+"/csvFile/",savePath=currentDir+"/soccerMatrixData/"):
	fileList=os.listdir(filepath)
	for filename in fileList:
		cutAndSave(filepath+filename,savePath)

def makePoint(filepath=currentDir+"/dataPoint/datapoint.pkl",k=10):
	f=open(filepath,"rb")
	dic=pickle.load(f)
	key=dic.keys()
	itemList=[]
	for item in key:
		#  shape of itemList will be like this:
		#  A_x_x            A_x_y    A_y_x   A_y_y  ...  
		# [(bowP,kClass )    (..)    (..)    (..)   ...   ] <- 2 items' tuple
		#  bowPoint has the shape of:
		# [ player1List,player2List...]
		itemList.append(bow(dic[item],k))

	playerNum=len(itemList[0][0])
	playerList=[]
	for j in range(playerNum):
		tmp=[]
		for ll in itemList:
			tmp.extend(ll[0][j])
		playerList.append(tmp)
	KMeansClass=[jj[1] for jj in itemList]

	return playerList,KMeansClass

def slimData(playerList,nComponents):
	pca=PCA(n_components=nComponents)
	pca.fit(playerList)
	return pca

def run(nComponents,k=10):
	playerList,KMeansClass=makePoint(k=k)
	pcaClass=slimData(playerList,nComponents)
	dic={"data":playerList,"pca":pcaClass,"KMeans":KMeansClass}
	filepath=currentDir+"/dataPoint/pca_"+str(k)+"_"+str(nComponents)+".pkl"
	f=open(filepath,"wb")
	pickle.dump(dic,f)

	return pcaClass.fit_transform(playerList)




