#!/usr/bin/env python
#created at 2019/11/3 遗传算法解决0-1背包问题

import random
import numpy as np
from matplotlib import pyplot as plt

#parameters
NP=50 #count of population
L=10 #count of gene
Pc=0.8 #crossover probability
Pm=0.05 #mutational probability
G=100 #count of generation
V=300 #bag volume
C=[95,75,23,73,50,22,6,57,89,98] #individual volume
W=[89,59,19,43,100,72,44,16,7,64] #individual value #targent:maxmize such sum of value
afa=2 #penalty coefficient

def fitness(f,C,W,V,afa):
	# fitness function:Total value
	fit=np.sum(f*W)
	TotalSize=np.sum(f*C)
	if(TotalSize>V):
		fit=fit-afa*(TotalSize-V) #penalty for the excess volume
	return fit

#population initialize
f=np.random.randint(0,2,size=(NP,L)) #binary coding
nf=np.zeros(shape=(NP,L))
Fit=np.zeros(NP)
trace=np.zeros(G)

#GA iteration
for k in range(G):
	for i in range(NP):
		Fit[i]=fitness(f[i,:],C,W,V,afa)
	maxFit=max(Fit)
	minFit=min(Fit)
	rr=np.argmax(Fit)
	fBest=f[rr,:]

	#select operator [roulette wheel selection]
	Fit=(Fit-minFit)/(maxFit-minFit) #fitness nomalization
	sum_Fit=sum(Fit)
	fitvalue=Fit/sum_Fit
	fitvalue=np.cumsum(fitvalue)
	ms=np.sort(np.random.rand(NP))
	fiti=0
	newi=0
	while(newi<NP):
		if(ms[newi]<fitvalue[fiti]):
			nf[newi,:]=f[fiti,:]
			newi+=1
		else:
			fiti+=1

	#crossover operator
	for i in range(0,NP,2):
		p=random.random() #(0,1)浮点数
		if(p<Pc):
			q=np.random.randint(0,2,size=(L))
			for j in range(L):
				if(q[j]==1):
					nf[i,j],nf[i+1,j]=nf[i+1,j],nf[i,j]

	#mutation operator
	for m in range(NP):
		for n in range(L):
			r=random.random()
			if(r<Pm):
				nf[m,n]=1 if(nf[m,n]==0) else 0

	#constract the new population
	f=np.array(list(nf)) #Don't f=nf,id(f)=if(nf),construct a new nf and subsequent assign to f!!!
	f[0]=fBest
	trace[k]=maxFit

plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
fig=plt.figure(figsize=(8,6))
plt.plot(trace)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()