#!/usr/bin/env python
#created at 2019/11/15 TS解决TSP问题

import numpy as np
from matplotlib import pyplot as plt

def target(D,s):
	DistanV=0
	n=len(s)
	for i in range(n-1):
		DistanV=DistanV+D[s[i],s[i+1]]
	DistanV=DistanV+D[s[n-1],s[0]]
	return DistanV

C=np.array([(1304,2312),(3639,1315),(4177,2244),(3712,1399),(3488,1535),(3226,1556),(3238,1229),(4196,1044),(4312,790),(4386,570),
(3007,1970),(2562,1756),(2788,1491),(2381,1676),(1332,695),(3715,1678),(3918,2179),(4061,2370),(3780,2212),(3676,2578),
(4029,2838),(4263,2931),(3429,1908),(3507,2376),(3394,2643),(3439,3201),(2935,3240),(3140,3550),(2545,2357),(2778,2826),(2370,2975)])
N=C.shape[0]
D=np.zeros(shape=(N,N))
for i in range(N):
	for j in range(N):
		D[i,j]=((C[i,0]-C[j,0])**2+(C[i,1]-C[j,1])**2)**0.5
Tabu=np.zeros(shape=(N,N))
TabuL=round((N*(N-1)/2)**0.5)
Ca=200
CaNum=np.zeros(shape=(Ca,N))
S0=np.random.permutation(np.arange(N))
bestsofar=S0
BestL=float('inf')
p=0
G=1000
ArrBestL=np.zeros(G)

while(p<G):
	i=0
	A=np.zeros(shape=(Ca,2)) #Ca个交换城市矩阵
	while(i<Ca):
		M=(N-1)*np.random.rand(2)
		M=np.ceil(M)
		if(M[0]!=M[1]):
			A[i,0]=max(M[0],M[1])
			A[i,1]=min(M[0],M[1])
			if(i==0):
				isa=0
			else:
				for j in range(i-1):
					if(A[i,0]==A[j,0] and A[i,1]==A[j,1]):
						isa=1
						break
					else:
						isa=0
			if(isa==0):
				i=i+1
	A=A.astype(int)
	BestCaNum=int(Ca/2)
	BestCa=np.ones(shape=(BestCaNum,4))
	F=np.zeros(Ca)
	for i in range(Ca):
		CaNum[i,:]=S0
		CaNum[i,[A[i,1],A[i,0]]]=S0[[A[i,0],A[i,1]]] #城市交换
		CaNum=CaNum.astype(int)
		F[i]=target(D,CaNum[i,:])
		if(i<BestCaNum):
			BestCa[i,0]=i
			BestCa[i,1]=F[i]
			BestCa[i,2]=S0[A[i,0]]
			BestCa[i,3]=S0[A[i,1]]
		else:
			for j in range(BestCaNum):
				if(F[i]<BestCa[j,1]):
					BestCa[j,0]=i
					BestCa[j,1]=F[i]
					BestCa[j,2]=S0[A[i,0]]
					BestCa[j,3]=S0[A[i,1]]
					break
	BestCa=BestCa[np.argsort(BestCa[:,1])] #N/2个优选路径
	BestCa=BestCa.astype(int)
	if(BestCa[0,1]<BestL):
		BestL=BestCa[0,1]
		S0=CaNum[BestCa[0,0],:]
		bestsofar=S0
		for m in range(N):
			for n in range(N):
				if(Tabu[m,n]!=0):
					Tabu[m,n]=Tabu[m,n]-1
		Tabu[BestCa[0,2],BestCa[0,3]]=TabuL
	else:
		for i in range(BestCaNum):
			if(Tabu[BestCa[i,2],BestCa[i,3]]==0):
				S0=CaNum[BestCa[i,0],:]
				for m in range(N):
					for n in range(N):
						if(Tabu[m,n]!=0):
							Tabu[m,n]=Tabu[m,n]-1
				Tabu[BestCa[i,2],BestCa[i,3]]=TabuL
				break
	ArrBestL[p]=BestL
	p=p+1

plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
fig=plt.figure(figsize=(16,6))

ax1=fig.add_subplot(121)
for i in range(N-1):
	ax1.plot([C[bestsofar[i],0],C[bestsofar[i+1],0]],[C[bestsofar[i],1],C[bestsofar[i+1],1]],'bo-')
ax1.plot([C[bestsofar[N-1],0],C[bestsofar[0],0]],[C[bestsofar[N-1],1],C[bestsofar[0],1]],'ro-')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

ax2=fig.add_subplot(122)
ax2.plot(ArrBestL)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()
