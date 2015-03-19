#!/usr/bin/python

import numpy as np
from math import sin,cos,asin,acos,sqrt

class zTransform(object):

	'''this class define a way to calculate the Z transform and make sample of the calculation result
	   plot func is also included in this class which and plot the result in z plane'''
	def __init__(self,dataArr,lag):
		self.dataArr=dataArr
		self.lag=lag
		
	
	def tran2AlgFunc(self,a,b):
		
		'''this func transfer the complex number from exponent form <a*(e**bj)> to Algebra form <x+y*j>.'''
		
		x=cos(b)*a
		y=sin(b)*a
		return x,y
		
	def tran2ExpFunc(self,x,y):
		
		'''this func transfer the complex number from Algebra form <x+y*j> to exponent form <a*(e**bj)>.'''
		
		a=sqrt(x**2+y**2)
		b=acos(x/a)
		c=asin(y/a)
		if x>=0 and  y>=0:
			return a,b
		elif x<0 and y>=0:
			return a,b
		elif x>=0 and y<0:
			return a,c
		elif x<0 and y<0:
			return a,-b

	def zTranFunc(self,A,theta):
		'''this Function trun the Z=A*(e**jr) theta is the angle and A is amplitude
		   input of this function is as the type of Z=A*(e**theta*j)
		   A-> float
		   theta-> float'''

		x_sample,y_sample=0,0

		for n in range(1,len(self.dataArr)+1):
			#turn every item in the shape of A*(e**theta*j) 
			A_one_tmp=self.dataArr[n-1]*(A**(-self.lag-n))
			theta_one_tmp=(-n-self.lag)*theta
			x_one_tmp,y_one_tmp=self.tran2AlgFunc(A_one_tmp,theta_one_tmp)

			x_sample+=x_one_tmp
			y_sample+=y_one_tmp

		A_sample,theta_sample=self.tran2ExpFunc(x_sample,y_sample)

		return A_sample,theta_sample

	def getSample(self,sampleList_theta,sampleList_A=None):
		'''this Function turn a bunch of samples into Z zTransform type
		   sampleList_theta is the theta samples and sampleList_A is the amplitude samples which are set to be all 1 list as default'''

		if sampleList_A==None:
			sampleList_A=[1]*len(sampleList_theta)

		A_list,theta_list=[],[]

		for i in range(len(sampleList_theta)):
			A_sample_,theta_sample_=self.zTranFunc(sampleList_A[i],sampleList_theta[i])
			A_list.append(A_sample_)
			theta_list.append(theta_sample_)
		return A_list,theta_list
		
