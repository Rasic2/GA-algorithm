#!/usr/bin/env python
#created at 2019/10/31 遗传算法实现f(x)=x+10sin(5x)+7cos(4x)最大值问题

import math
import random
from functools import reduce
import numpy as np
from matplotlib import pyplot as plt

def fit(x):
	y=x+10*math.sin(5*x)+7*math.cos(4*x)
	return y

def genetic_algorithm(x,y):
	NP=50;L=20;Pc=0.8;Pm=0.1;G=100;Xs=10;Xx=0
	f=np.random.randint(0,2,size=(NP,L)) #Np*L维数组,元素只有0和1

	trace=np.zeros(shape=G)
	for k in range(G):
		X=np.zeros(shape=(NP))
		Fit=np.zeros(shape=(NP))
		for i in range(NP):
			U=int(reduce(lambda x,y:x+y,f[i,:].astype(str)),2) #二进制字符串转化为十进制:np.array=>str,reduce元素累加,int进制转换
			X[i]=Xx+U*(Xs-Xx)/(2**L-1) #定义域内十进制
			Fit[i]=fit(X[i])

		maxFit=max(Fit)
		minFit=min(Fit)
		fbest=f[np.argmax(Fit),:] #最优个体
		xbest=X[np.argmax(Fit)] #最优个体的x坐标
		Fit=(Fit-minFit)/(maxFit-minFit) #最大最小值归一化

		fit_value=np.cumsum(Fit/sum(Fit)) #适应度权重
		ms=np.sort(np.random.rand(NP)) #轮盘赌随机概率,NP个(0,1)的浮点数

		#选择算子
		fiti=0
		newi=0
		nf=np.zeros(shape=(NP,L))
		while(newi<=NP-1):
			if(ms[newi]<fit_value[fiti]):
				nf[newi,:]=f[fiti,:]
				newi+=1
			else:
				fiti+=1

		#交叉算子
		for i in range(0,NP,2):
			p=random.random() #(0,1)浮点数
			if(p<Pc):
				q=np.random.randint(0,2,size=(L))
				for j in range(L):
					if(q[j]==1):
						nf[i,j],nf[i+1,j]=nf[i+1,j],nf[i,j]

		#变异算子
		i=1
		while(i<=round(NP*Pm)): #四舍五入
			h=random.randint(0,NP-1) #(0,NP-1)中一个随机整数
			for j in range(round(L*Pm)):
				g=random.randint(0,L-1)
				nf[h,g]=1 if(nf[h,g]==0) else 0 #取反
			i+=1

		f=nf.astype(int)
		f[1,:]=fbest
		trace[k]=maxFit
	return trace

def main():
	x=np.arange(0,10,0.01)
	y=x+10*np.sin(5*x)+7*np.cos(4*x)
	trace=genetic_algorithm(x,y)
	plt.rc('font',family='Times New Roman') #配置全局字体
	plt.rcParams['mathtext.default']='regular' #配置数学公式字体
	plt.rcParams['lines.linewidth']=3 #配置线条宽度
	plt.rcParams['lines.markersize']=7 #配置标记大小
	fig=plt.figure(figsize=(16,6))

	ax1=fig.add_subplot(121)
	ax1.plot(x,y)
	plt.xticks(fontsize=18)
	plt.yticks(fontsize=18)

	ax2=fig.add_subplot(122)
	plt.plot(trace)
	plt.xticks(fontsize=18)
	plt.yticks(fontsize=18)
	plt.show()

if __name__ == '__main__':
	main()


