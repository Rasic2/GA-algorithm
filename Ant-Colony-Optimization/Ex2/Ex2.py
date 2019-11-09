#!/usr/bin/env python
#created at 2019/11/9 蚁群算法解决f(x,y)=20(x^2-y^2)^2-(1-y)^2-3(1+y)^2+0.3

import random
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import FuncFormatter

m=20
G=200
Rho=0.9
P0=0.2
XMAX=5
XMIN=-5
YMAX=5
YMIN=-5
X=np.zeros(shape=(m,2))
Tau=np.zeros(m)

def target(x,y):
	value=20*(x**2-y**2)**2-(1-y)**2-3*(1+y)**2+0.3
	return value

for i in range(m):
	X[i,0]=(XMIN+(XMAX-XMIN)*random.random())
	X[i,1]=(XMIN+(XMAX-XMIN)*random.random())
	Tau[i]=target(X[i,0],X[i,1])

step=0.1
P=np.zeros(shape=(G,m))
trace=np.zeros(G)
for NC in range(G):
	lamda=1/(NC+1)
	BestIndex=np.argmin(Tau)
	for i in range(m):
		P[NC,i]=(Tau[BestIndex]-Tau[i])/Tau[BestIndex]
	for i in range(m):
		if(P[NC,i]<P0):
			temp1=X[i,0]+(2*random.random()-1)*step*lamda
			temp2=X[i,0]+(2*random.random()-1)*step*lamda
		else:
			temp1=X[i,0]+(XMAX-XMIN)*(random.random()-0.5)
			temp2=X[i,0]+(XMAX-XMIN)*(random.random()-0.5)
		if(temp1<XMIN):
			temp1=XMIN
		if(temp1>XMAX):
			temp1=XMAX
		if(temp2<XMIN):
			temp2=XMIN
		if(temp2>XMAX):
			temp2=XMAX
		if(target(temp1,temp2)<target(X[i,0],X[i,1])):
			X[i,0],X[i,1]=temp1,temp2
	for i in range(m):
		Tau[i]=(1-Rho)*Tau[i]+target(X[i,0],X[i,1])
	index=np.argmin(Tau)
	trace[NC]=target(X[index,0],X[index,1])

def format_tick(x,pos):
    return '$%d$' % (x/1000)

def format_bar(x,pos):
    return r'${0}$'.format(int(x/1000))

plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
plt.rcParams['font.size']=16
fig=plt.figure(figsize=(16,6))

ax1=fig.add_subplot(121,projection='3d')
X=np.arange(-5,5,0.01).reshape(1000,1)
Y=np.arange(-5,5,0.01).reshape(1,1000)
Z=20*(X**2-Y**2)**2-(1-Y)**2-3*(1+Y)**2+0.3
surf=ax1.plot_surface(X,Y,Z,cmap=cm.coolwarm,linewidth=0,antialiased=False)
formatter=FuncFormatter(format_tick)
ax1.zaxis.set_major_formatter(formatter) #刻度缩小100000倍
ax1.text(5,5,13500,r'$×10^3$')
ax1.tick_params(labelsize=18) #setting fontsize of [x|y|z]ticks
fig.colorbar(surf,shrink=0.5,aspect=5,format=FuncFormatter(format_bar))

ax2=fig.add_subplot(122)
ax2.plot(trace)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()

