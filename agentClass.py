#! /usr/bin/python

import math
import random

class agent(object):
	'''
	this class is the agent that have models including run romdomly, chasing.
	we add some noise into the vision that the predicted distance may not be exactly the same as the real one
	the noise is decided by the real distance that if the distance get larger the noise will grow.
	'''
#this is the agent with position(x and y) to show the agent's condition#
        def __init__(self,init_x,init_y):
		self.x=init_x
		self.y=init_y
		self.velocity_x=0
		self.velocity_y=0
		self.last_x=init_x
		self.last_y=init_y

	def updateAgent(self):
		self.last_x=self.x
		self.last_y=self.y

		#update the next one
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

	def decideVelKeepDis(self,chased,DisToMatain,vel,threshold=0.3):
			#this one is the velocity decision function to keep a certain distance with other agent
			#the vel is velocity of the agent in a range of [vel_min,vel_max]


			dist=math.sqrt((chased.x-self.x)**2+(chased.y-self.y)**2)
			error_x=random.normalvariate(0,dist*0.1)
			error_y=random.normalvariate(0,dist*0.1)
			vision_x=chased.x+error_x
			vision_y=chased.y+error_y
			
			visionDist=math.sqrt((vision_x-self.x)**2+(vision_y-self.y)**2)
			if visionDist-DisToMatain<=threshold:
				self.velocity_x+=random.normalvariate(0,vel*0.05)
				self.velocity_y+=random.normalvariate(0,vel*0.05)
			elif visionDist-DisToMatain>threshold:
				if visionDist<=vel[1] and visionDist>=vel[0]:
					self.velocity_x=vision_x+random.normalvariate(0,vel*0.05)-self.x
					self.velocity_y=vision_y+random.normalvariate(0,vel*0.05)-self.y
				elif visionDist<vel[0]:
					self.velocity_x=(vision_x-self.x)/visionDist*vel[0]+random.normalvariate(0,vel*0.05)
					self.velocity_y=(vision_y-self.y)/visionDist*vel[0]+random.normalvariate(0,vel*0.05)
				elif visionDist>vel[1]:
					self.velocity_x=(vision_x-self.x)/visionDist*vel[0]+random.normalvariate(0,vel*0.05)
					self.velocity_y=(vision_y-self.y)/visionDist*vel[0]+random.normalvariate(0,vel*0.05)

	def runningToPoint(self,point,vel):
		#this function make the agent running to a certain point with speed vel. point is a list [x,y].
		dist=math.sqrt((point[0]-self.x)**2+(point[1]-self.y)**2)
		error_x=random.normalvariate(0,dist*0.01)
		error_y=random.normalvariate(0,dist*0.01)
		vision_x=point[0]+error_x
		vision_y=point[1]+error_y
			
		visionDist=math.sqrt((vision_x-self.x)**2+(vision_y-self.y)**2)
		
		self.velocity_x=(point[0]-self.x)/visionDist*vel+random.normalvariate(0,vel*0.05)
		self.velocity_y=(point[1]-self.y)/visionDist*vel+random.normalvariate(0,vel*0.05)
	
	def runningParallel(self,referenceAgent):
			#if the agent is chasing one, use this function to decide the speed#
			dist=math.sqrt((referenceAgent.x-self.x)**2+(referenceAgent.y-self.y)**2)
			error_x=random.normalvariate(0,dist*0.005)
			error_y=random.normalvariate(0,dist*0.005)
			#print error_x,"and",error_y
			
			self.velocity_x=referenceAgent.velocity_x+error_x
			self.velocity_y=referenceAgent.velocity_y+error_y
		

