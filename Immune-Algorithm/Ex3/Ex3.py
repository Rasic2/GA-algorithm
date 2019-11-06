#!/usr/bin/env python
#created at 2019/11/6 免疫算法求解TSP问题

import random
import numpy as np
from matplotlib import pyplot as plt

from fortfunc import fort_floor as floor
from fortfunc import target

#parameters
NP=200
G=500
Ncl=10
C=np.array([(1304,2312),(3639,1315),(4177,2244),(3712,1399),(3488,1535),(3226,1556),(3238,1229),(4196,1044),(4312,790),(4386,570),
(3007,1970),(2562,1756),(2788,1491),(2381,1676),(1332,695),(3715,1678),(3918,2179),(4061,2370),(3780,2212),(3676,2578),
(4029,2838),(4263,2931),(3429,1908),(3507,2376),(3394,2643),(3439,3201),(2935,3240),(3140,3550),(2545,2357),(2778,2826),(2370,2975)])
N=C.shape[0]
D=np.zeros(shape=(N,N)) #城市距离矩阵,N*N
for i in range(N):
	for j in range(N):
		D[i,j]=((C[i,0]-C[j,0])**2+(C[i,1]-C[j,1])**2)**0.5

f=np.zeros((NP,N))
for i in range(NP):
	f[i,:]=np.random.permutation(np.arange(N))
f=f.astype(int)
length=np.zeros(NP)
for i in range(NP):
	length[i]=target(f[i,:],D)

Sortlength_arg=np.argsort(length)
Sortf=f[Sortlength_arg,:]

#种群迭代
gen=0
trace=np.zeros(G)
while(gen<G):
	af=np.zeros(shape=(int(NP/2),N))
	alen=np.zeros(int(NP/2))
	Calength=np.zeros(Ncl)
	for i in range(int(NP/2)):
		a=Sortf[i,:]
		Ca=np.tile(a,(Ncl,1)) #clone operation
		#mutatation operator
		for j in range(Ncl):
			p1=floor(N*random.random())
			p2=floor(N*random.random())
			while(p1==p2):
				p1=floor(N*random.random())
				p2=floor(N*random.random())
			Ca[j,p1],Ca[j,p2]=Ca[j,p2],Ca[j,p1]
		Ca[0,:]=a #remain the origin
		#clone inhibitation
		Ca=Ca.astype(int)
		for j in range(Ncl):
			Calength[j]=target(Ca[j,:],D)
		af[i]=Ca[np.argmin(Calength)]
		alen[i]=np.min(Calength)

	#flush population
	bf=np.zeros((int(NP/2),N))
	blen=np.zeros(int(NP/2))
	for i in range(int(NP/2)):
		bf[i,:]=np.random.permutation(np.arange(N))
		bf=bf.astype(int)
		blen[i]=target(bf[i,:],D)

	#construct the new population
	f1=np.concatenate((af,bf)) #np.concatenate(()) double (())
	length=np.concatenate((alen,blen))
	Sortlength_arg=np.argsort(length)
	Sortf=f1[Sortlength_arg]
	trace[gen]=np.min(length)
	gen=gen+1

Bestf=Sortf[0].astype(int)

plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
fig=plt.figure(figsize=(16,6))

ax1=fig.add_subplot(121)
for i in range(N-1):
	ax1.plot([C[Bestf[i],0],C[Bestf[i+1],0]],[C[Bestf[i],1],C[Bestf[i+1],1]],'bo-')
ax1.plot([C[Bestf[N-1],0],C[Bestf[0],0]],[C[Bestf[N-1],1],C[Bestf[0],1]],'ro-')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

ax2=fig.add_subplot(122)
ax2.plot(trace)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()

