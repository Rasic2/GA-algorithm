#!/usr/bin/env python
#created at 2019/11/12 PSO算法求解f(x)=x+6sin(4x)+9cos(5x)最小值问题

import math
import random
from functools import reduce
import numpy as np
from matplotlib import pyplot as plt

def target(X,Xmax,Xmin):
	D=len(X)
	m=int(reduce(lambda x,y:x+y,X.astype(str)),2) #二进制字符串转化为十进制:np.array=>str,reduce元素累加,int进制转换
	f=Xmin+m*(Xmax-Xmin)/(2**D-1) #定义域内十进制
	result=f+6*math.sin(4*f)+9*math.cos(5*f)
	return result

#paramaters
N=100
D=20
T=200
c1=1.5
c2=1.5
Wmax=0.8
Wmin=0.4
Xmax=9
Xmin=0
Vmax=10
Vmin=-10

#initalization
x=np.random.randint(0,2,size=(N,D))
v=np.random.rand(N,D)*(Vmax-Vmin)+Vmin
p=np.array(list(x))
pbest=np.ones(N)
for i in range(N):
	pbest[i]=target(x[i,:],Xmax,Xmin)
g=p[np.argmin(pbest)]
gbest=np.min(pbest)
gb=np.ones(T)

#iteration
vx=np.zeros(shape=(N,D))
for i in range(T):
	for j in range(N):
		if(target(x[j,:],Xmax,Xmin)<pbest[j]):
			p[j,:]=x[j,:]
			pbest[j]=target(x[j,:],Xmax,Xmin)
		if(pbest[j]<gbest):
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
fig=plt.figure(figsize=(16,6))

ax1=fig.add_subplot(121)
X=np.arange(0,9,0.01)
Y=X+6*np.sin(4*X)+9*np.cos(5*X)
ax1.plot(X,Y)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

ax2=fig.add_subplot(122)
ax2.plot(gb)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()