#!/usr/bin/env python
#created at 2019/11/1 遗传算法实现f(x)=∑x_i^{2}最小值问题

import random
import numpy as np
from matplotlib import pyplot as plt

def genetic_algorithm():
	NP=100;D=10;Pc=0.8;Pm=0.1;G=1000;Xs=20;Xx=-20
	f=np.zeros(shape=(NP,D))
	nf=np.zeros(shape=(NP,D))
	f=np.random.rand(NP,D)*(Xs-Xx)+Xx #初始化种群,实数编码
	MSLL=np.argsort(np.sum(f**2,axis=1)) #按升序排列好之后对应索引值
	Sortf=f[MSLL,:]

	trace=np.zeros(shape=G)
	for gen in range(G):
		#君主方案进行交叉操作
		Emper=Sortf[0,:] #适应度最高认为是君主
		NoPoint=round(D*Pc) #交叉基因个数
		PoPint=np.random.randint(0,D,size=(int(NP/2),NoPoint)) #交叉基因数组
		nf=Sortf
		for i in range(int(NP/2)):
			nf[2*i,:]=Emper #奇数子代为雄性君主
			nf[2*i+1,:]=Sortf[2*i+1,:] #偶数子代为雌性
			for k in range(NoPoint):
				nf[2*i,PoPint[i,k]]=nf[2*i+1,PoPint[i,k]] #君主与偶数第一位交叉,两个后代,奇数位为君主+交叉过来的偶数部分
				nf[2*i+1,PoPint[i,k]]=Emper[PoPint[i,k]] #偶数位为偶数+交叉过来的君主部分
		#变异操作
		for m in range(NP):
			for n in range(D):
				r=random.random()
				if(r<Pm):
					nf[m,n]=random.random()*(Xs-Xx)+Xx
		#子代父代合并,选取前NP个个体
		SortfMSLL=np.argsort(np.concatenate((np.sum(Sortf**2,axis=1),np.sum(nf**2,axis=1))))[:NP]
		Sortf=np.concatenate((Sortf,nf))[SortfMSLL,:]
		trace[gen]=np.sum(Sortf**2,axis=1)[0]
	return trace

def main():
	trace=genetic_algorithm()
	plt.rc('font',family='Times New Roman') #配置全局字体
	plt.rcParams['mathtext.default']='regular' #配置数学公式字体
	plt.rcParams['lines.linewidth']=3 #配置线条宽度
	plt.rcParams['lines.markersize']=7 #配置标记大小
	fig=plt.figure(figsize=(8,6))
	plt.plot(trace)
	plt.xticks(fontsize=18)
	plt.yticks(fontsize=18)
	plt.show()

if __name__ == '__main__':
	main()

