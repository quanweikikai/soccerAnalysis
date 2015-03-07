#! /usr/bin/python

import math
import random

class agent(object):
	'''
	this class is the agent that have models including run romdomly, chasing.
	'''
#this is the agent with position(x and y) to show the agent's condition#
        def __init__(self,init_x,init_y):
		self.x=init_x
		self.y=init_y
		self.velocity_x=0
		self.velocity_y=0

	def updateAgent(self):
		self.x+=self.velocity_x
		self.y+=self.velocity_y
		
	def decideVelChasing(self,chased,vel):
			#if the agent is chasing one, use this function to decide the speed#
			dist=math.sqrt((chased.x-self.x)**2+(chased.y-self.y)**2)
			error_x=random.normalvariate(0,dist*0.1)
			error_y=random.normalvariate(0,dist*0.1)
			vision_x=chased.x+error_x
			vision_y=chased.y+error_y
			
			visionDist=math.sqrt((vision_x-self.x)**2+(vision_y-self.y)**2)
			self.velocity_x=(vision_x-self.x)/visionDist*vel
			self.velocity_y=(vision_y-self.y)/visionDist*vel

	def decideVelChased(self,vel):
			#if the agent is chased one, use this function to decide the speed#
		if self.velocity_x==0 and self.velocity_y==0:
			angle=random.uniform(0,math.pi)
			self.velocity_x=math.sin(angle)
			self.velocity_y=math.cos(angle)
		else:
			vel=math.sqrt((self.velocity_x)**2+(self.velocity_y)**2)
			self.velocity_x+=random.normalvariate(0,vel*0.05)
			self.velocity_y+=random.normalvariate(0,vel*0.05)

		
