#!/usr/bin/env python
#created at 2019/11/12 PSO解决f(x)=∑x^(2)最小值问题

import random
import numpy as np
from matplotlib import pyplot as plt

#paramaters
N=100
D=10
T=200
c1=1.5
c2=1.5
w=0.8
Xmax=20
Xmin=-20
Vmax=10
Vmin=-10

#initalization
x=np.random.rand(N,D)*(Xmax-Xmin)+Xmin
v=np.random.rand(N,D)*(Vmax-Vmin)+Vmin
p=np.array(list(x))
pbest=np.sum(x**2,axis=1)
g=p[np.argmin(pbest)]
gbest=np.min(pbest)
gb=np.ones(T)

#iteration
for i in range(T):
	for j in range(N):
		if(np.sum(x[j,:]**2)<pbest[j]):
			p[j,:]=x[j,:]
			pbest[j]=np.sum(x[j,:]**2)
		if(pbest[j]<gbest):
			g=p[j,:]
			gbest=pbest[j]
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
fig=plt.figure(figsize=(8,6))
plt.plot(gb)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()