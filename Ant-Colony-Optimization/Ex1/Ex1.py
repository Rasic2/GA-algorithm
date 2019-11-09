#!/usr/bin/env python
#created at 2019/11/8 蚁群算法解决TSP问题

import math
import random
import numpy as np
from matplotlib import pyplot as plt

#paramaters
m=50 #count of ants
alpha=1 #pheromone factor
beta=5 #inspring factor
rho=0.1 #decay factor
G=200 #count of iteration
Q=100 #pheromone enhancement factor
eps=2.2204**-16

#initialization
C=np.array([(1304,2312),(3639,1315),(4177,2244),(3712,1399),(3488,1535),(3226,1556),(3238,1229),(4196,1044),(4312,790),(4386,570),
(3007,1970),(2562,1756),(2788,1491),(2381,1676),(1332,695),(3715,1678),(3918,2179),(4061,2370),(3780,2212),(3676,2578),
(4029,2838),(4263,2931),(3429,1908),(3507,2376),(3394,2643),(3439,3201),(2935,3240),(3140,3550),(2545,2357),(2778,2826),(2370,2975)])
N=C.shape[0]
D=np.zeros(shape=(N,N))
for i in range(N):
	for j in range(N):
		if(i!=j):
			D[i,j]=((C[i,0]-C[j,0])**2+(C[i,1]-C[j,1])**2)**0.5
		else:
			D[i,j]=eps
Eta=1.0/D #inspring
Tau=np.ones(shape=(N,N)) #pheromone
Tabu=np.zeros(shape=(m,N)) #path list
NC=0
R_best=np.zeros(shape=(G,N))
L_best=np.ones(G) #best length


#iteration
while(NC<G):
	Randpos=[]
	for i in range(math.ceil(m/N)):
		Randpos+=list(np.random.permutation(np.arange(N)))
	Tabu[:,0]=Randpos[0:m] #start city of the m ants
	for j in range(1,N): #城市巡游
		for i in range(m):
			visited=Tabu[i,0:j].astype(int) #numpy切片[a,b) j个已访问城市列表
			J=np.zeros(N-j).astype(int) #N-j个待访问城市
			Jc=0
			for k in range(N):
				if(k not in visited):
					J[Jc]=k
					Jc=Jc+1
			P=[] #待访问城市访问概率
			for k in range(len(J)):
				P.append((Tau[visited[-1],J[k]]**alpha)*(Eta[visited[-1],J[k]]**beta)) #距离和信息素浓度双重判定
			P=P/sum(P)
			Pcum=np.cumsum(P)
			Select=np.where(Pcum>=random.random())
			while(len(Select[0])==0):
				Select=np.where(Pcum>=random.random())
			to_visit=J[Select[0][0]] #随机选取第一个访问
			Tabu[i,j]=to_visit
	if(NC>=1):
		Tabu[0,:]=R_best[NC-1,:] #保留上一代最好路径
	L=np.zeros(m)
	for i in range(m):
		R=Tabu[i,:].astype(int)
		for j in range(N-1):
			L[i]=L[i]+D[R[j],R[j+1]]
		L[i]=L[i]+D[R[0],R[N-1]]
	L_best[NC]=min(L) #巡游路径长度
	R_best[NC,:]=Tabu[np.argmin(L),:]

	delta_Tau=np.zeros(shape=(N,N)) #距离增强矩阵
	Tabu=Tabu.astype(int)
	for i in range(m):
		for j in range(N-1):
			delta_Tau[Tabu[i,j],Tabu[i,j+1]]=delta_Tau[Tabu[i,j],Tabu[i,j+1]]+Q/L[i]
		delta_Tau[Tabu[i,N-1],Tabu[i,0]]=delta_Tau[Tabu[i,N-1],Tabu[i,0]]+Q/L[i]
	Tau=(1-rho)*Tau+delta_Tau #当前信息素浓度
	Tabu=np.zeros(shape=(m,N)) #清空路径信息
	NC=NC+1

R_best=R_best.astype(int)
plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
fig=plt.figure(figsize=(16,6))

ax1=fig.add_subplot(121)
for i in range(N-1):
	ax1.plot([C[R_best[-1,i],0],C[R_best[-1,i+1],0]],[C[R_best[-1,i],1],C[R_best[-1,i+1],1]],'bo-')
ax1.plot([C[R_best[-1,N-1],0],C[R_best[-1,0],0]],[C[R_best[-1,N-1],1],C[R_best[-1,0],1]],'ro-')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

ax2=fig.add_subplot(122)
ax2.plot(L_best)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()





