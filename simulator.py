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
		#prepare the list to write data
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
				print chasingAgent.velocity_x,"  ",chasingAgent.velocity_y

			dataList.append(oneDataList)
			print oneDataList

	pickle.dump(dataList,output)




	   
	   
	

