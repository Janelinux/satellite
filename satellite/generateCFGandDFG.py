import os
import re
import numpy as np
import pandas as pd 
import networkx as nx   

def CFGgeneration (path):

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

def generate_ListandGraph (path):

    os.chdir(path)   
    if os.path.getsize('contract.tac')>0:
        b=pd.read_table("contract.tac",delimiter='\n',header=None)
    else:
        b=pd.DataFrame(columns = ["3IR"])
        line=pd.Series({"3IR":"0"}) 
        b=b.append(line,ignore_index=True)       

    k=0
    b.columns = ["3IR"]
    b['blockname']='0'
    b['leftvariable']='0'
    b['rightvariable']='0'
    b['option']='0'
    b['function']='0'


    for i in range(0,len(b)):
        blockindex=b.iloc[i,0].find('block')
        if blockindex>0:
            k=b.iloc[i,0][(blockindex+6):]
            b.iloc[i,1]=k
            #print (b.iloc[i,0][(blockindex+6):])
        b.iloc[i,1]=k
        bsplit=re.split(r'(?:[, : \s ( )])',b.iloc[i,0])
        #print(bsplit)
        if (bsplit.count('=')>0):
            eindex=bsplit.index('=')
            b.iloc[i,4]=bsplit[eindex+1]
            #print (bsplit[eindex])
            for p in range(0,eindex):
                findvar=bsplit[p]
            
                if (findvar.find('v')>-1):
                    b.iloc[i,2]= findvar
        
            for p in range(eindex,len(bsplit)):
                if (bsplit[p].find('v')>-1):
                    b.iloc[i,3]=b.iloc[i,3]+','+ bsplit[p]
        else:
            if(len(bsplit)>7 and b.iloc[i,0].find('succ')<0):
                b.iloc[i,4]=bsplit[6]
                for p in range(0,len(bsplit)):
                    if (bsplit[p].find('v')>-1):
                        b.iloc[i,3]=b.iloc[i,3]+','+ bsplit[p]

        if(b.iloc[i,0].find("function")>-1):
            fun_split=re.split(r'(?:[ ( )])',b.iloc[i,0])
            b.iloc[i,5]=fun_split[1]
        else:
            b.iloc[i,5]=b.iloc[(i-1),5] 
    graph_index = pd.DataFrame(columns = ["current", "prev", "succ"])



    for k in range(0,len(b)):
        if(b.iloc[k,0].find("prev")>-1):
            graph_split=re.split(r'(?:[=\[\]])',b.iloc[k,0])
            #print(graph_split[2])
            #print(graph_split[5])
            if(len(graph_split)>6):
                line=pd.Series({"current":b.iloc[k,1],"prev":graph_split[2],"succ":graph_split[5]})
                graph_index=graph_index.append(line,ignore_index=True)

    return  [b, graph_index]  

def DFG_edge (b):
    edge=[]
    
    for i in range(0,len(b)):
        if(b.iloc[i,2]!="0" and b.iloc[i,3]!="0" ):
            
            right_split=re.split(r'(?:[ , ])',b.iloc[i,3])
            if(len(right_split)==3):
                edge.append([right_split[1], b.iloc[i,2], b.iloc[i,4]])
                edge.append([right_split[2], b.iloc[i,2], b.iloc[i,4]])
            if(len(right_split)==2):
                edge.append([right_split[1], b.iloc[i,2], b.iloc[i,4]])
    return edge


def DFGgeneration (edge):
    DFG=nx.DiGraph()#创建空的简单有向图
    for n in range (0, len(edge)):
        DFG.add_edge(edge[n][0], edge[n][1])
    return DFG


#path = "/pro/decom/cross-chain-bugs/.temp/QBridge/out"  
#[b, graph_index]=generate_ListandGraph (path)
#print(b)
#dfg_edge = DFG_edge(b)
#print(dfg_edge)
#print(graph_index)
#DFG=DFGgeneration(dfg_edge)
#print(list(nx.all_neighbors(DFG,'v2202Vf1a')))


#python3 generateCFGandDFG.py