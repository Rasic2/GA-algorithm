#!/usr/bin/env python
#created at 2019/11/4 差分进化算法解决f(x)=∑x^(2)最小值问题

import math
import random
import numpy as np
from matplotlib import pyplot as plt

#parameters
NP=50      #count of population
D=10       #count of genes
G=600      #count of generation
F0=0.4     #initial mutation factor
CR=0.1     #crossover factor
Xs=20      #upper bound
Xx=-20     #lower bound
yz=10**-6  #convergence threshold

#initialize population
x=np.zeros((NP,D))
v=np.zeros((NP,D))
u=np.zeros((NP,D))
x=np.random.rand(NP,D)*(Xs-Xx)+Xx
Ob=np.sum(x**2,axis=1).reshape(NP,1)
trace=np.zeros(G)
trace[0]=min(Ob)

#DE iteration
for gen in range(G):

	#calculate the mutation factor
	λ=math.exp(1-G/(G+1-gen))
	F=F0*2**λ

	#mutation operator
	for m in range(NP):
		r1=random.randint(0,NP-1) #closed interval [a,b]
		while(r1==m):
			r1=random.randint(0,NP-1)
		r2=random.randint(0,NP-1)
		while(r2==m or r2==r1):
			r2=random.randint(0,NP-1)
		r3=random.randint(0,NP-1)
		while(r3==m or r3==r2 or r3==r1):
			r3=random.randint(0,NP-1)
		v[m,:]=x[r1,:]+F*(x[r2,:]-x[r3,:])

	#crossover operator
	r=random.randint(0,D-1)
	for n in range(D):
		cr=random.random()
		if(cr<=CR or n==r):
			u[:,n]=v[:,n]
		else:
			u[:,n]=v[:,n]

	#bondary condition
	u=np.where((u<Xx)|(u>Xs),random.random()*(Xs-Xx)+Xx,u) #vetorize the ndarray

	#select operator
	Ob1=np.sum(u**2,axis=1).reshape(NP,1)
	x=np.where(Ob1<Ob,u,x)
	Ob=np.sum(x**2,axis=1).reshape(NP,1)
	trace[gen]=min(Ob)
	if(min(Ob)<yz):
		break

plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
fig=plt.figure(figsize=(8,6))
plt.plot(trace[trace!=0])
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()