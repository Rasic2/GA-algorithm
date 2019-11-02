#!/usr/bin/env python
#created at 2019/11/1 遗传算法实现路径最小化问题,有问题??优化振荡,不收敛
#created at 2019/11/2 random.sample() 随机返回列表元素,修改后会影响原列表值

import math
import random
import numpy as np
from matplotlib import pyplot as plt

C=[(1304,2312),(3639,1315),(4177,2244),(3712,1399),(3488,1535),(3226,1556),(3238,1229),(4196,1004),(4312,790),(4386,570),
(3007,1970),(2562,1756),(2788,1491),(2381,1676),(1332,695),(3715,1678),(3918,2179),(4061,2370),(3780,2212),(3676,2578),
(4029,2838),(4263,2931),(3429,1908),(3507,2367),(3394,2643),(3439,3201),(2935,3240),(3140,3550),(2545,2357),(2778,2826),(2370,2975)]
C=np.array(C)
N=C.shape[0]
D=np.zeros((N,N)) #城市距离矩阵,N*N
for i in range(N):
	for j in range(N):
		D[i,j]=((C[i,0]-C[j,0])**2+(C[i,1]-C[j,1])**2)**0.5

#初始化种群
NP=200;G=2000
f=np.zeros((NP,N))
for i in range(NP):
	f[i,:]=np.random.permutation(np.arange(N))
f=f.astype(int)
F=[]
R=f[0,:]
length=np.zeros(NP)
fitness=np.zeros(NP)

#种群迭代
gen=0
Rlength=np.zeros(G)
while(gen<G):
	for i in range(NP):
		length[i]=D[f[i,N-1],f[i,0]]
		for j in range(N-1):
			length[i]=length[i]+D[f[i,j],f[i,j+1]]

	maxlen=max(length)
	minlen=min(length)
	rr=np.argmin(length)
	R=f[rr,:] #父代最优路径
	for i in range(len(length)):
		fitness[i]=(1-((length[i]-minlen)/(maxlen-minlen+0.001)))
	#选择算子
	for i in range(NP):
		rand=random.random()
		if(fitness[i]>=rand): #怀疑子代选择有问题,并不是朝适应度更高的方向移动
			F.append(f[i,:])
	aa=len(F)
	while(aa<NP):
		A,B=random.sample(F,2) #选取F列表中两个样本用于后续交叉变异操作 !!!random.sample()返回列表memoryview,值会变化
		A,B=np.array(list(A)),np.array(list(B))
		#交叉算子
		W=math.ceil(N/10)
		p=random.randint(0,N-W-1)
		for i in range(W):
			x=np.where(A==B[p+i-1])
			y=np.where(B==A[p+i-1])
			A[p+i-1],B[p+i-1]=B[p+i-1],A[p+i-1]
			A[x],B[y]=B[y],A[x]
		#变异算子
		p1=math.floor(N*random.random())
		p2=math.floor(N*random.random())
		while(p1==p2):
			p1=math.floor(N*random.random())
			p2=math.floor(N*random.random())
		A[p1],A[p2]=A[p2],A[p1] #交换p1、p2值进行变异
		B[p1],B[p2]=B[p2],B[p1]
		A=A.reshape(1,N)
		B=B.reshape(1,N)
		F=F+list(A)+list(B)
		aa=len(F)
	if(aa>NP):
		F=F[0:NP]
	f=np.array(F)
	f[0,:]=R
	F=[]
	Rlength[gen]=minlen
	gen+=1

plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
fig=plt.figure(figsize=(16,6))

ax1=fig.add_subplot(121)
for i in range(N-1):
	ax1.plot([C[R[i],0],C[R[i+1],0]],[C[R[i],1],C[R[i+1],1]],'bo-')
ax1.plot([C[R[N-1],0],C[R[0],0]],[C[R[N-1],1],C[R[0],1]],'ro-')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

ax2=fig.add_subplot(122)
ax2.plot(Rlength)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()
