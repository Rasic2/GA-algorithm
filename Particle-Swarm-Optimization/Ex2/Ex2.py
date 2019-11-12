#!/usr/bin/env python
#created at 2019/11/12 PSO解决f(x,y)=3cos(xy)+x+y^2最小值问题

import random
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#paramaters
N=100
D=2
T=200
c1=1.5
c2=1.5
Wmax=0.8
Wmin=0.4
Xmax=4
Xmin=-4
Vmax=1
Vmin=-1

#initalization
x=np.random.rand(N,D)*(Xmax-Xmin)+Xmin
v=np.random.rand(N,D)*(Vmax-Vmin)+Vmin
p=np.array(list(x))
pbest=3*np.cos(x[:,0]*x[:,1])+x[:,0]+x[:,1]**2
g=p[np.argmin(pbest)]
gbest=np.min(pbest)
gb=np.ones(T)

#iteration
for i in range(T):
	for j in range(N):
		if((3*np.cos(x[j,0]*x[j,1])+x[j,0]+x[j,1]**2)<pbest[j]):
			p[j,:]=x[j,:]
			pbest[j]=3*np.cos(x[j,0]*x[j,1])+x[j,0]+x[j,1]**2
		if(pbest[j]<gbest):
			g=p[j,:]
			gbest=pbest[j]
		w=Wmax-(Wmax-Wmin)*(i/T)
		v[j,:]=w*v[j,:]+c1*random.random()*(p[j,:]-x[j,:])+c2*random.random()*(g-x[j,:])
		x[j,:]=x[j,:]+v[j,:]

		for ii in range(D):
			if(v[j,ii]>Vmax or v[j,ii]<Vmin):
				v[j,ii]=random.random()*(Vmax-Vmin)+Vmin
			if(x[j,ii]>Xmax or x[j,ii]<Xmin):
				x[j,ii]=random.random()*(Xmax-Xmin)+Xmin
	gb[i]=gbest

plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
plt.rcParams['font.size']=16
fig=plt.figure(figsize=(16,6))

ax1=fig.add_subplot(121,projection='3d')
X=np.arange(-4,4,0.02).reshape(400,1)
Y=np.arange(-4,4,0.02).reshape(1,400)
Z=3*np.cos(X*Y)+X+Y**2
surf=ax1.plot_surface(X,Y,Z,cmap=cm.coolwarm,linewidth=0,antialiased=False)
ax1.tick_params(labelsize=18) #setting fontsize of [x|y|z]ticks
fig.colorbar(surf,shrink=0.5,aspect=5)

ax2=fig.add_subplot(122)
ax2.plot(gb)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()