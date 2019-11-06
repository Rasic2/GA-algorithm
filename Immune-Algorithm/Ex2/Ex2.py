#!/usr/bin/env python
#created at 2019/11/6 免疫算法解决f(x,y)=5sin(xy)+x^2+y^2最小值问题

import random
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from EulerDist import distance

#parameters
NP=50     #count of B cells
D=2       #count of genes
G=200      #count of generation
pm=0.7     #mutation factor
α=2		   #exciation coefficient
β=1		   #exciation coefficient
δ=0.2      #similarity threshold
Ncl=5     #count of clone
Xs=4      #upper bound
Xx=-4     #lower bound
Δ0=0.5*Xs    #neighbourhood range

def target(x):
	value=(5*np.sin(x[:,0]*x[:,1])+x[:,0]**2+x[:,1]**2)
	return value

def exciation(f,MSLL,NP,α=2,β=1,δ=0.2):
	#exciation function
	nd=np.zeros(NP)
	ND=np.zeros(NP)
	for i in range(NP):
		for j in range(NP):
			nd[j]=distance(f[i,:],f[j,:])
		nd=np.where(nd<δ,1,0)
		ND[i]=np.sum(nd)/NP #concentation
	MSLL=α*MSLL-β*ND
	return MSLL

#initialize population
f=np.random.rand(NP,D)*(Xs-Xx)+Xx
MSLL=target(f)
MSLL=exciation(f,MSLL,NP) #calculate degrees of exciation
SortMSLL_arg=np.argsort(MSLL)
Sortf=f[SortMSLL_arg,:]

#DE iteration
gen=0
trace=np.zeros(G)
while(gen<G):
	af=np.zeros(shape=(int(NP/2),D))
	aMSLL=np.zeros(int(NP/2))
	for i in range(int(NP/2)):
		a=Sortf[i,:]
		Na=np.tile(a,(Ncl,1)) #clone operation
		Δ=Δ0/(gen+1) #real neighbourhood
		#mutatation operator
		for j in range(Ncl):
			for ii in range(D):
				if(random.random()<pm):
					Na[j,ii]=Na[j,ii]+(random.random()-0.5)*Δ
		Na=np.where(((Na>Xs)|(Na<Xx)),random.random()*(Xs-Xx)+Xx,Na)
		Na[0,:]=a #remain the origin
		#clone inhibitation
		NaMSLL=target(Na)
		af[i]=Na[np.argmin(NaMSLL)]
		aMSLL[i]=np.min(NaMSLL)
	aMSLL=exciation(af,aMSLL,int(NP/2))

	#flush population
	bf=np.random.rand(int(NP/2),D)*(Xs-Xx)+Xx
	bMSLL=target(bf)
	bMSLL=exciation(bf,bMSLL,int(NP/2))

	#construct the new population
	f1=np.concatenate((af,bf)) #np.concatenate(()) double (())
	MSLL1=np.concatenate((aMSLL,bMSLL))
	SortMSLL1_arg=np.argsort(MSLL1)
	Sortf=f1[SortMSLL1_arg]
	trace[gen]=np.min(target(f1))
	gen=gen+1

plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
fig=plt.figure(figsize=(16,6))
ax1=fig.add_subplot(121,projection='3d')
X=np.arange(-4,4,0.02).reshape(400,1)
Y=np.arange(-4,4,0.02).reshape(1,400)
Z=5*np.sin(X*Y)+X**2+Y**2
surf=ax1.plot_surface(X,Y,Z,cmap=cm.coolwarm,linewidth=0,antialiased=False)
ax1.tick_params(labelsize=18)

ax2=fig.add_subplot(122)
plt.plot(trace)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()

