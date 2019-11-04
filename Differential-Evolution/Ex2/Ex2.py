#!/usr/bin/env python
#created at 2019/11/4 差分进化算法解决f(x,y)=3cos(xy)+x+y最小值问题

import math
import random
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#parameters
NP=20     #count of population
D=2       #count of genes
G=100     #count of generation
F=0.5     #initial mutation factor
CR=0.1    #crossover factor
Xs=4      #upper bound
Xx=-4     #lower bound

#initialize population
x=np.zeros((NP,D))
v=np.zeros((NP,D))
u=np.zeros((NP,D))
x=np.random.rand(NP,D)*(Xs-Xx)+Xx
Ob=(3*np.cos(x[:,0]*x[:,1])+x[:,0]+x[:,1]).reshape(NP,1)
trace=np.zeros(G)
trace[0]=min(Ob)

#DE iteration
for gen in range(G):

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
	u=np.where(u<Xx,Xx,u) #vetorize the ndarray
	u=np.where(u>Xs,Xs,u) #vetorize the ndarray

	#select operator
	Ob1=(3*np.cos(u[:,0]*u[:,1])+u[:,0]+u[:,1]).reshape(NP,1)
	x=np.where(Ob1<Ob,u,x)
	Ob=(3*np.cos(x[:,0]*x[:,1])+x[:,0]+x[:,1]).reshape(NP,1)
	trace[gen]=min(Ob)

plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
plt.rcParams['font.size']=16
fig=plt.figure(figsize=(16,6))

ax1=fig.add_subplot(121,projection='3d')
X=np.arange(-4,4,0.02).reshape(400,1)
Y=np.arange(-4,4,0.02).reshape(1,400)
Z=3*np.cos(X*Y)+X+Y
surf=ax1.plot_surface(X,Y,Z,cmap=cm.coolwarm,linewidth=0,antialiased=False)
ax1.tick_params(labelsize=18) #setting fontsize of [x|y|z]ticks
fig.colorbar(surf,shrink=0.5,aspect=5)

ax2=fig.add_subplot(122)
ax2.plot(trace)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()
