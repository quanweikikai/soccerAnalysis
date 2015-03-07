#! /usr/bin/python
import pickle

def reader(filename='data.pkl'):
	dataFile=open(filename,'rb')
	dataList=pickle.load(dataFile)
	return dataList
	
