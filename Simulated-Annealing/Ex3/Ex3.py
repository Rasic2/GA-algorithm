#!/usr/bin/env python
#created at 2019/11/14 SA算法解决TSP问题

import math
import random
from collections import namedtuple
import numpy as np
from matplotlib import pyplot as plt

def target(citys,n):
	length=0
	for i in range(n-1):
		length=length+math.sqrt((citys[i].x-citys[i+1].x)**2+(citys[i].y-citys[i+1].y)**2)
	length=length+math.sqrt((citys[n-1].x-citys[0].x)**2+(citys[n-1].y-citys[0].y)**2)
	return length

C=np.array([(1304,2312),(3639,1315),(4177,2244),(3712,1399),(3488,1535),(3226,1556),(3238,1229),(4196,1044),(4312,790),(4386,570),
(3007,1970),(2562,1756),(2788,1491),(2381,1676),(1332,695),(3715,1678),(3918,2179),(4061,2370),(3780,2212),(3676,2578),
(4029,2838),(4263,2931),(3429,1908),(3507,2376),(3394,2643),(3439,3201),(2935,3240),(3140,3550),(2545,2357),(2778,2826),(2370,2975)])
n=C.shape[0]
T=100*n
L=100
K=0.99
city=namedtuple('city',['x','y'])
citys=[city(item[0],item[1]) for item in C]
length=[]
length.append(target(citys,n))
while(T>0.001):
	for i in range(L):
		len1=target(citys,n)
		p1=math.floor(n*random.random())
		p2=math.floor(n*random.random())
		while(p1==p2):
			p1=math.floor(n*random.random())
			p2=math.floor(n*random.random())
		tmp_citys=list(citys)
		tmp_citys[p1],tmp_citys[p2]=tmp_citys[p2],tmp_citys[p1]
		len2=target(tmp_citys,n)
		delta_e=len2-len1
		if(delta_e<0):
			citys=list(tmp_citys)
		else:
			if(math.exp(-delta_e/T)>random.random()):
				citys=list(tmp_citys)
	length.append(target(citys,n))
	T=T*K

plt.rc('font',family='Times New Roman') #配置全局字体
plt.rcParams['mathtext.default']='regular' #配置数学公式字体
plt.rcParams['lines.linewidth']=3 #配置线条宽度
plt.rcParams['lines.markersize']=7 #配置标记大小
fig=plt.figure(figsize=(16,6))

ax1=fig.add_subplot(121)
for i in range(n-1):
	ax1.plot([citys[i].x,citys[i+1].x],[citys[i].y,citys[i+1].y],'bo-')
ax1.plot([citys[n-1].x,citys[0].x],[citys[n-1].y,citys[0].y],'ro-')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

ax2=fig.add_subplot(122)
ax2.plot(length)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()
