#! /usr/bin/python
import math
import random
from agentClass import *
import pickle
	

def chasingSimulator(numOfAgent,frameNum):
#chasedClass are the agent that being chased, chasingClass are the agents that chasing the chased one
	#initial all the agents
	#frame number-> the total number of data frame

	chasedAgent=agent(0,0)
	#list to save the chasing agent
	chasingList=[]
	for i in range(numOfAgent-1):
		init_x=random.choice([-1,1])*random.randint(100,200)
		init_y=random.choice([-1,1])*random.randint(100,200)
		chasingAgent=agent(init_x,init_y)
		chasingList.append(chasingAgent)

	#prepare the file to write data
	output=open("data.pkl","wb")
	#prepare the list to save data
	dataList=[]

	#start chasing
	for index in range(frameNum):
			chasedAgent.decideVelChased(4)
			oneDataList=[chasedAgent.x,chasedAgent.y]
			chasedAgent.updateAgent()
			for chasingAgent in chasingList:
				chasingAgent.decideVelChasing(chasedAgent,5)
				oneDataList.extend([chasingAgent.x,chasingAgent.y])
				chasingAgent.updateAgent()

			dataList.append(oneDataList)

	pickle.dump(dataList,output)

def simulatorRunToPoint(numOfAgent,frameNum,filename="dataRun2P"):
	agentList=[]
	for i in range(numOfAgent):
		init_x=random.choice([-1,1])*random.randint(1800,2200)
		init_y=random.choice([-1,1])*random.randint(1800,2200)
		chasingAgent=agent(init_x,init_y)
		agentList.append(chasingAgent)
	#prepare the file to write data
	output=open(filename,"wb")
	#prepare the list to save data
	dataList=[]

	#start chasing
	for index in range(frameNum):
		oneDataList=[]
		for oneAgent in agentList:
			oneAgent.runningToPoint([0,0],3)
			oneAgent.updateAgent()
			oneDataList.extend([oneAgent.x,oneAgent.y])
		
		dataList.append(oneDataList)

	pickle.dump(dataList,output)

def simulatorRunningParallel(numOfAgent,frameNum,filename=" "):
	agentList=[]
	reference=agent(0,0)
	agentList.append(reference)

	for i in range(numOfAgent-1):
		init_x=random.choice([-1,1])*random.randint(0,100)
		init_y=random.choice([-1,1])*random.randint(0,100)
		chasingAgent=agent(init_x,init_y)
		agentList.append(chasingAgent)
	
	#prepare the file to write data
	output=open(filename,"wb")
	#prepare the list to save data
	dataList=[]

	#start chasing
	for index in range(frameNum):
		oneDataList=[]
		agentList[0].decideVelChased(1)
		oneDataList.extend([agentList[0].x,agentList[0].y])
		agentList[0].updateAgent()
		for h in range(1,numOfAgent):
			agentList[h].runningParallel(agentList[0])
			
			#for test
			#print agentList[h].velocity_x
			#print agentList[h].velocity_y


			oneDataList.extend([agentList[h].x,agentList[h].y])
			agentList[h].updateAgent()
		
		dataList.append(oneDataList)

	pickle.dump(dataList,output)

def makeDataRun2P(num):
		prefix="makeDataRun2P_"
		postfix=".pkl"
		for i in range(num):
			filename=prefix+str(i)+postfix
			simulatorRunToPoint(5,600,filename)

def makeDataRunParallel(num):
		prefix="makeDataRunParallel"
		postfix=".pkl"
		for i in range(num):
			filename=prefix+str(i)+postfix
			simulatorRunningParallel(5,600,filename)

