#!/usr/bin/env python
#created at 2019/11/14 SA算法解决f(x,y)=5cos(xy)+xy+y^3最小值问题

import random
import math
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def target(x,y):
	value=5*math.cos(x*y)+x*y+y**3
	return value

Xmax=5
Xmin=-5
Ymax=5
Ymin=-5
L=100
K=0.99
S=0.02
T=100
YZ=1e-8

PreX=random.random()*(Xmax-Xmin)+Xmin
PreY=random.random()*(Ymax-Ymin)+Ymin
PreBestX=PreX
PreBestY=PreY
PreX=random.random()*(Xmax-Xmin)+Xmin
PreY=random.random()*(Ymax-Ymin)+Ymin
BestX=PreX
BestY=PreY

trace=[]
deta=abs(target(BestX,BestY)-target(PreBestX,PreBestY))
while(deta>YZ and T>0.001):
	T=K*T
	for i in range(L):
		p=0
		while(p==0):
			NextX=PreX+S*(random.random()*(Xmax-Xmin)+Xmin)
			NextY=PreX+S*(random.random()*(Ymax-Ymin)+Ymin)
			if(NextX>=Xmin and NextX<=Xmax and NextY>=Ymin and NextY<=Ymax):
				p=1
		if(target(BestX,BestY)>target(NextX,NextY)):
			PreBestX,BestX=BestX,NextX
			PreBestY,BestY=BestY,NextY
		if(target(PreX,PreY)>target(NextX,NextY)):
			PreX=NextX
			PreY=NextY
		else:
			changer=-1*(target(NextX,NextY)-target(PreX,PreY))/T
			p1=math.exp(changer)
			if(p1>random.random()):
				PreX=NextX
				PreY=NextY
	trace.append(target(BestX,BestY))
	deta=abs(target(BestX,BestY)-target(PreBestX,PreBestY))

plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
fig=plt.figure(figsize=(16,6))

ax1=fig.add_subplot(121,projection='3d')
X=np.arange(-5,5,0.02).reshape(500,1)
Y=np.arange(-5,5,0.02).reshape(1,500)
Z=5*np.cos(X*Y)+X*Y+Y**3
surf=ax1.plot_surface(X,Y,Z,cmap=cm.coolwarm,linewidth=0,antialiased=False)
ax1.tick_params(labelsize=18)

ax2=fig.add_subplot(122)
plt.plot(trace)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()

