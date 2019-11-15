#!/usr/bin/env python
#created at 2019/11/15 TS解决f(x,y)=(cos(x^2+y^2)-0.1)/(1+0.3(x^2+y^2)^2)+3最大值问题

import math
import random
import numpy as np
from collections import namedtuple
from matplotlib import cm
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def target(x):
	y=(math.cos(x[0]**2+x[1]**2)-0.1)/(1+0.3*(x[0]**2+x[1]**2)**2)+3
	return y

xu=5
xl=-5
L=random.randint(5,11)
Ca=5
G=200
w=1
tabu=[]
x0=np.random.rand(2)*(xu-xl)+xl
bestsofar_nt=namedtuple('bestsofal_nt',['key','value'])
bestsofar=bestsofar_nt(x0,target(x0))
xnow_nt=namedtuple('xnow_nt',['key','value'])
xnow=np.array([xnow_nt for i in range(G)])
xnow[0]=xnow_nt(x0,target(x0))
candidate_nt=namedtuple('candidate_nt',['key','value'])
candidate=np.array([candidate_nt for i in range(G)])

g=0
trace=np.zeros(G)
while(g<G-1):
	x_near=np.zeros(shape=(Ca,2))
	fitvalue_near=np.zeros(Ca)
	w=w*0.998
	for i in range(Ca):
		x_temp=xnow[g].key
		x1=x_temp[0]
		x2=x_temp[1]

		x_near[i,0]=x1+(2*random.random()-1)*w*(xu-xl)
		if(x_near[i,0]<xl):
			x_near[i,0]=xl
		if(x_near[i,0]>xu):
			x_near[i,0]=xu

		x_near[i,1]=x2+(2*random.random()-1)*w*(xu-xl)
		if(x_near[i,1]<xl):
			x_near[i,1]=xl
		if(x_near[i,1]>xu):
			x_near[i,1]=xu

		fitvalue_near[i]=target(x_near[i,:])
	temp=x_near[np.argmax(fitvalue_near),:]
	candidate[g]=candidate_nt(temp,target(temp))
	delta1=candidate[g].value-xnow[g].value
	delta2=candidate[g].value-bestsofar.value
	if(delta1<=0):
		xnow[g+1]=xnow_nt(candidate[g].key,xnow[g].value)
		tabu.append(xnow[g+1].key)
		if(len(tabu)>L):
			tabu=[]
		g=g+1
	elif(delta2>0):
		xnow[g+1]=xnow_nt(candidate[g].key,candidate[g].value)
		tabu.append(xnow[g+1].key)
		if(len(tabu)>L):
			tabu=[]
		bestsofar=bestsofar_nt(candidate[g].key,candidate[g].value)
		g=g+1
	else:
		r=0
		for m in range(len(tabu)):
			if(candidate[g].key(0)==tabu[m][0] and candidate[g].key(1)==tabu[m][1]):
				r=1
		if(r==0):
			xnow[g+1]=xnow_nt(candidate[g].key,candidate[g].value)
			tabu.append(xnow[g+1].key)
			if(len(tabu)>L):
				tabu=[]
			g=g+1
		else:
			xnow[g]=xnow_nt(xnow[g].key,xnow[g].value)
	trace[g]=bestsofar.value

plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
fig=plt.figure(figsize=(16,6))

ax1=fig.add_subplot(121,projection='3d')
X=np.arange(-5,5,0.01).reshape(1000,1)
Y=np.arange(-5,5,0.01).reshape(1,1000)
Z=(np.cos(X**2+Y**2)-0.1)/(1+0.3*(X**2+Y**2)**2)+3
surf=ax1.plot_surface(X,Y,Z,cmap=cm.coolwarm,linewidth=0,antialiased=False)
ax1.tick_params(labelsize=18)

ax2=fig.add_subplot(122)
plt.plot(trace)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()