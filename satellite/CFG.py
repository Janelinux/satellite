# -*- coding: utf-8 -*-
import os
import re
import numpy as np
import pandas as pd 
import networkx as nx   
from Procession import *




def xCFG (path):

    os.chdir(path)   #修改当前工作目录

    #intra-procedure CFG

    G=nx.DiGraph()#创建空的简单有向图
    if os.path.getsize('LocalBlockEdge.csv')>0:
        controledge = pd.read_csv("LocalBlockEdge.csv",delimiter='\t',header=None)      #control edge
    else:
        controledge =[]

    if os.path.getsize('IRFunction_Return.csv')>0:
        returnedge=pd.read_csv("IRFunction_Return.csv",delimiter='\t',header=None)      #return edge
    else:
        returnedge=[]

    if os.path.getsize('IRFunctionCall.csv')>0:
        calledge=pd.read_csv("IRFunctionCall.csv",delimiter='\t',header=None)           #call edge
    else:
        calledge=[]

    #print(calledge)

    if os.path.getsize('PublicFunction.csv')>0:
        externedge=pd.read_csv("PublicFunction.csv",delimiter='\t',header=None)    #externedge
    else:
        externedge=[]

    controllength=len(controledge)
    returnlength=len(returnedge)
    calllength=len(calledge)
    externlength=len(externedge)


    for i in range(0,controllength): #1515097                             #add control edge
        G.add_edge(controledge.iloc[i,0],controledge.iloc[i,1])

    functions=list(nx.weakly_connected_components(G))

    #print('Functions list',functions)

    for i in range(0,externlength): #1515097                              #add extern edge DOS attack without these edge
        G.add_edge("extern_node",externedge.iloc[i,0])

    for i in range(0,calllength): #1515097                              #add return edge
        for j in range(0,returnlength):
            if calledge.iloc[i,1]==returnedge.iloc[j,0]:
                G.add_edge(returnedge.iloc[j,1],calledge.iloc[i,0])



    return G











# python3 xCFG.py