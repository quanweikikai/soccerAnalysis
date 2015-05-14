#! /usr/bin/python
#####################################################################################
#----------------------------------bagOfWords.py------------------------------------
#TODO this one turn an inputArrayList into bag of words list
#TODO 1.unwrap all the arrayList in inputArrList
#     inputArrList has the shape like this:
#     player1            player2              player3
#  [Arr1,Arr2... ]     [Arr1,Arr2...]       [...     ]
#TODO 2.put all the points into space and use KMeans algorithm to cluster points
#TODO 3.count every cluster's number and make the bag of words list
# made by Ken in 2015.05.10
# latest modified in 2015.05.13
#####################################################################################

import sklearn.cluster.k_means_ as km

def bow(inputArrList,clusterNum=5):
	unfoldedList=[]
	for i in inputArrList:
		unfoldedList.extend(i)
		
	kmeansClass=km.KMeans(k=clusterNum)
	kmeansClass.fit(unfoldedList)

	bowPoint=[]
	setList=range(clusterNum)
	for j in inputArrList:
		result=kmeansClass.predict(j)
		result=result.tolist()
		resultSize=len(result)
		oneBowPoint=[]
		for l in setList:
			oneBowPoint.append(result.count(l)/float(resultSize))
		bowPoint.append(oneBowPoint)
	return bowPoint,kmeansClass
	
	






