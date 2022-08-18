# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 23:19:54 2021

@author: LENOVO
"""


import numpy as np
import itertools 
import random
import pandas as pd

def generate_ParityCheckMatrix(n,m,D):
  A=np.zeros((m,n),dtype=int)
  #S=set(range(0,m))
  #combs=list(itertools.combinations(S,D))
  #K=len(combs)
  print("Parity Check Matrix")
  print(40*"_")
  for i in range(0,n):
    while(np.sum(A[:,i])<D):
      j=random.randint(0,m-1)
      A[j,i]=1
  print(A)
  print(40*"_")
  return A


def generate_codewords(A,n):
  S=set(range(0,n))
  x=np.zeros(n,dtype=int)
  #print(x)
  tot=1
  min_weight=n
  for i in range(1,n):
    combs=list(itertools.combinations(S,i))
    for t in combs:
      x=np.zeros(n,dtype=int)
      t=list(t)
      x[t]=1
      y=np.dot(A,x)
      if(not np.sum(y%2)):
        #print(x)
        tot+=1
        if(i<min_weight):
          min_weight=i
  print("n               :",n)
  print("m               :",m)
  print("1-m/n           :",1-m/n)
  print("rate            :", np.log2(tot)/n)
  print("minimum_distance: ",min_weight)
  print(40*"_")
  
def get_neighbors(A,x,n,m):
  x=list(x)
  total=0
  
  for i in range(0,m):
    if(np.sum(A[i,x])!=0):
      total+=1
    

  return total


def get_parameters_expander(A,n,m,D):
  min_neighbors=[D]
  S=set(range(0,n))
  mini=m
  for i in range(2,n+1):
    combinations=list(itertools.combinations(S,i))
    mini=m
    for combi in combinations:
      neighs=get_neighbors(A,combi,n,m)
      mini=min(neighs,mini)

    min_neighbors.append(mini)
  
  #print(min_neighbors)
  return min_neighbors

def get_exp_props(min_neigbors,n,m,D):
  mod_S=np.array(list(range(1,n+1)))
  mod_NS=np.array(min_neighbors)
  gamma=mod_S/n
  alpha_dash=mod_NS/mod_S
  alpha=np.zeros(n)
  alpha[0]=alpha_dash[0]
  for i in range(1,n):
    alpha[i]=min(alpha[i-1],alpha_dash[i])

  one_minus_eps=alpha/D
  epsilon=1-one_minus_eps
  deltas= 2*n*gamma*(one_minus_eps)
  relative_deltas=deltas/n
  
  data={'epsilon': epsilon, 'gamma' : gamma, '2*gamma*n*(1-eps)':deltas}
  df=pd.DataFrame(data,columns=['epsilon','gamma','2*gamma*n*(1-eps)'])
  print(df)


n=16
m=10
D=4

A=generate_ParityCheckMatrix(n,m,D)
codes=generate_codewords(A,n)
min_neighbors=get_parameters_expander(A,n,m,D)

get_exp_props(min_neighbors,n,m,D)


