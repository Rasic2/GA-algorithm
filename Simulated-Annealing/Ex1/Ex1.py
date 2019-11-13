#!/usr/bin/env python
#created at 2019/11/13 SA算法解决f(x)=∑x^(2)最小值问题

import random
import math
import numpy as np
from matplotlib import pyplot as plt

D=10
Xmax=20
Xmin=-20
L=200
K=0.998
S=0.01
T=100
YZ=1e-8

PreX=np.random.rand(D)*(Xmax-Xmin)+Xmin
PreBestX=np.array(list(PreX))
PreX=np.random.rand(D)*(Xmax-Xmin)+Xmin
BestX=np.array(list(PreX))

trace=[]
deta=abs(np.sum(BestX**2)-np.sum(PreBestX**2))
while(deta>YZ and T>0.01):
	T=K*T
	print(T)
	for i in range(L):
		NextX=PreX+S*(np.random.rand(D)*(Xmax-Xmin)+Xmin)
		NextX=np.where((NextX>Xmax)|(NextX<Xmin),PreX+S*(random.random()*(Xmax-Xmin)+Xmin),NextX)
		if(np.sum(BestX**2)>np.sum(NextX**2)):
			PreBestX,BestX=BestX,NextX
		if(np.sum(PreX**2)>np.sum(NextX**2)):
			PreX=NextX
		else:
			changer=-1*(np.sum(NextX**2)-np.sum(PreX**2))/T
			p1=math.exp(changer)
			if(p1>random.random()):
				PreX=NextX
	trace.append(np.sum(BestX**2))
	deta=abs(np.sum(BestX**2)-np.sum(PreBestX**2))

plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
fig=plt.figure(figsize=(8,6))
plt.plot(trace)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()