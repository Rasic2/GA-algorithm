#!/usr/bin/env python
#created at 2019/11/5 差分进化算法解决f(x,y)=-((x^2+y-1)^2+(x+y^2-7)^2)/200+10最大值问题

import math
import random
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import FuncFormatter

#parameters
NP=20     #count of population
D=2       #count of genes
G=100     #count of generation
F=0.5     #initial mutation factor
CR=0.1    #crossover factor
Xs=100    #upper bound
Xx=-100   #lower bound

#initialize population
x=np.zeros((NP,D))
v=np.zeros((NP,D))
u=np.zeros((NP,D))
x=np.random.randint(Xx,Xs+1,size=(NP,D))
Ob=(-((x[:,0]**2+x[:,1]-1)**2+(x[:,0]+x[:,1]**2-7)**2)/200+10).reshape(NP,1)
trace=np.zeros(G)
trace[0]=max(Ob)

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
		v[m,:]=np.floor((x[r1,:]+F*(x[r2,:]-x[r3,:])))

	#crossover operator
	r=random.randint(0,D-1)
	for n in range(D):
		cr=random.random()
		if(cr<=CR or n==r):
			u[:,n]=v[:,n]
		else:
			u[:,n]=x[:,n]

	#bondary condition
	u=np.where(u<Xx,Xx,u) #vetorize the ndarray
	u=np.where(u>Xs,Xs,u) #vetorize the ndarray

	#select operator
	Ob1=(-((u[:,0]**2+u[:,1]-1)**2+(u[:,0]+u[:,1]**2-7)**2)/200+10).reshape(NP,1)
	x=np.where(Ob1>Ob,u,x)
	Ob=(-((x[:,0]**2+x[:,1]-1)**2+(x[:,0]+x[:,1]**2-7)**2)/200+10).reshape(NP,1)
	trace[gen]=max(Ob)

def format_tick(x,pos):
    return '$%d$' % (x/100000)

def format_bar(x,pos):
    return r'${0}$'.format(int(x/100000))

plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
plt.rcParams['font.size']=16
fig=plt.figure(figsize=(16,6))

ax1=fig.add_subplot(121,projection='3d')
X=np.arange(-100,100,1).reshape(200,1)
Y=np.arange(-100,100,1).reshape(1,200)
Z=(-((X**2+Y-1)**2+(X+Y**2-7)**2)/200+10)
surf=ax1.plot_surface(X,Y,Z,cmap=cm.coolwarm,linewidth=0,antialiased=False)
formatter=FuncFormatter(format_tick)
ax1.zaxis.set_major_formatter(formatter) #刻度缩小100000倍
ax1.tick_params(labelsize=18) #setting fontsize of [x|y|z]ticks
ax1.text(85,130,0,r'$×10^5$')
fig.colorbar(surf,shrink=0.5,aspect=5,format=FuncFormatter(format_bar))

ax2=fig.add_subplot(122)
ax2.plot(trace)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()
