#!/usr/bin/python

import numpy as np
from math import sin,cos,asin,acos,sqrt

import warnings

warnings.simplefilter('error',RuntimeWarning)

def checkNan(num):
	if num>-10000000000 and num<1000000000000:
		return False
	else:
		return True



class zTransform(object):

	'''this class define a way to calculate the Z transform and make sample of the calculation result
	   plot func is also included in this class which and plot the result in z plane
	   dataArrList is a list with the shape of [Arr1,Arr2,Arr3...]'''
	def __init__(self,dataArrList,lag,index):
		self.dataArrList=dataArrList
		self.lag=lag
		#index takes the type of [0,1,2,3] or in this case [0,3]
		self.index=index
		
	
	def tran2AlgFunc(self,a,b):
		
		'''this func transfer the complex number from exponent form <a*(e**bj)> to Algebra form <x+y*j>.'''
		
		x=cos(b)*a
		y=sin(b)*a
		return x,y
		
	def tran2ExpFunc(self,x,y):
		
		'''this func transfer the complex number from Algebra form <x+y*j> to exponent form <a*(e**bj)>.'''
		
		a_=sqrt(x**2+y**2)
		#sometimes both x and y will equal to 0 and this will lead to an error(RuntimeWarning make the return value a NaN ones)
		try:
			b=np.arccos(x/a_)
			c=np.arcsin(y/a_)
		except Warning:
			a_=0
			b=0
			c=0
		if x>=0 and  y>=0:
			return a_,b
		elif x<0 and y>=0:
			return a_,b
		elif x>=0 and y<0:
			return a_,c
		elif x<0 and y<0:
			return a_,-b

	def zTranFunc(self,A,theta):
		'''this Function trun the Z=A*(e**jr) theta is the angle and A is amplitude
		   input of this function is as the type of Z=A*(e**theta*j)
		   this func open every item in dataArrList and sum all the samples together.
		   A-> float
		   theta-> float'''

		x_sample,y_sample=0,0

		for m in range(len(self.dataArrList)):
			#for n in range(1,len(self.dataArrList[0])+1):
			for n in range(len(self.index)):
				#turn every item in the type of A*(e**theta*j) 
				A_one_tmp=self.dataArrList[m][n]*(A**(-self.lag-self.index[n]))
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
			if checkNan(A_sample_) or checkNan(theta_sample_):
				print sampleList_A[i]," ",sampleList_theta[i]
				print self.dataArrList

			A_list.append(A_sample_)
			theta_list.append(theta_sample_)
		return A_list,theta_list
		
