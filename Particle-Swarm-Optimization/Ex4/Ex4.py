#!/usr/bin/env python
#created at 2019/11/13 PSO算法解决0-1背包问题

import random
import numpy as np
from matplotlib import pyplot as plt

def target(x,C,W,V,afa):
	fit=np.sum(x*W)
	TotalSize=np.sum(x*C)
	if(TotalSize<=V):
		fit=fit
	else:
		fit=fit-afa*(TotalSize-V)
	return fit

#paramaters
N=100
D=10
T=200
c1=1.5
c2=1.5
Wmax=0.8
Wmin=0.4
Vmax=10
Vmin=-10
V=300
C=[95,75,23,73,50,22,6,57,89,98] #individual volume
W=[89,59,19,43,100,72,44,16,7,64] #individual value #targent:maxmize such sum of value
afa=2

#initalization
x=np.random.randint(0,2,size=(N,D))
v=np.random.rand(N,D)*(Vmax-Vmin)+Vmin
p=np.array(list(x))
pbest=np.ones(N)
for i in range(N):
	pbest[i]=target(x[i,:],C,W,V,afa)
g=p[np.argmax(pbest)]
gbest=np.max(pbest)
gb=np.ones(T)

#iteration
vx=np.zeros(shape=(N,D))
for i in range(T):
	for j in range(N):
		if(target(x[j,:],C,W,V,afa)>pbest[j]):
			p[j,:]=x[j,:]
			pbest[j]=target(x[j,:],C,W,V,afa)
		if(pbest[j]>gbest):
			g=p[j,:]
			gbest=pbest[j]
		w=Wmax-(Wmax-Wmin)*(i/T)
		v[j,:]=w*v[j,:]+c1*random.random()*(p[j,:]-x[j,:])+c2*random.random()*(g-x[j,:])

		for ii in range(D):
			if(v[j,ii]>Vmax or v[j,ii]<Vmin):
				v[j,ii]=random.random()*(Vmax-Vmin)+Vmin
		vx[j,:]=1/(1+np.exp(-v[j,:]))
		for jj in range(D):
			if(vx[j,jj]>random.random()):
				x[j,jj]=1
			else:
				x[j,jj]=0
	gb[i]=gbest

plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
plt.rcParams['font.size']=16
fig=plt.figure(figsize=(8,6))

plt.plot(gb)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()