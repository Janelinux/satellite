import os
import re
import numpy as np 
import pandas as pd
import networkx as nx
import csv
import time
from generateCFGandDFG import *

def find_statevariable (path,b):
    #path = "/pro/decom/FSE/gigahorse/gigahorse-toolchain/.temp/new/out"                           # 设置路径
    os.chdir(path)   #修改当前工作目录


    #state-dependency edge
    SD_edge=[]
    #find sload state variable, struct, array, mapping
    for j in range(0,len(b)):
        sloadindex=b.iloc[j,0].find('SLOAD')
        if (sloadindex>0):   
            sloadstatement=b.iloc[j,0][(sloadindex+5):]
            addressindex=sloadstatement.find('(')
            if(addressindex>0):  ##find state variable, struct, array
                stateaddress=sloadstatement[(addressindex+1):]
                stateaddressmodify=stateaddress[:(len(stateaddress)-1)]
                state_var='stor_'+stateaddressmodify
                #print([state_var,b.iloc[j,1]]) ##modify here
                SD_edge.append([state_var, b.iloc[j,1], b.iloc[j,3]])
            else:
                leftfind=[j]
                uloop=1
                findSHA3=0
                while(findSHA3<1 and uloop<10):
                    findSHA3=0
                    SHAsplit=[]
                    for m in range(0,len(leftfind)):
                        SHAsplit=list(set(SHAsplit+re.split(r'(?:[,])',b.iloc[leftfind[m],3])))
                    #print('SHAsplit',SHAsplit)
                    leftfind=[]
                    for n in range(0,len(SHAsplit)):
                        if (SHAsplit[n]!='0' and b.iloc[:,2].tolist().count(SHAsplit[n])>0):
                             leftfind.append(b.iloc[:,2].tolist().index(SHAsplit[n]))
                             #print('leftfind',leftfind)
                    for m in range(0,len(leftfind)):
                        if (b.iloc[leftfind[m],4].find('SHA3')<0):
                            findSHA3=findSHA3 or 0
                        if (b.iloc[leftfind[m],4].find('SHA3')>-1):
                            findSHA3=findSHA3 or 1
                            #print(leftfind[m])
                            if(b.iloc[leftfind[m],0].count('(')>0 and b.iloc[leftfind[m],0].count(')')>0):
                                SHAaddress1=b.iloc[leftfind[m],0][b.iloc[leftfind[m],0].index('(')+1:b.iloc[leftfind[m],0].index(')')]
                            if(b.iloc[leftfind[m],0].count(')')>0):
                                delete=b.iloc[leftfind[m],0][b.iloc[leftfind[m],0].index(')')+1:] 
                            if(b.iloc[leftfind[m],0].count('(')>0 and b.iloc[leftfind[m],0].count(')')>0 and delete.count('(')>0 and delete.count(')')>0):
                                SHAaddress2=delete[delete.index('(')+1:delete.index(')')]
                                mapping='stor_'+SHAaddress1+'_'+SHAaddress2
                                SD_edge.append([mapping,b.iloc[j,1], b.iloc[j,3]])
                            #print([mapping,b.iloc[j,1]]) ##modify here
                    uloop=uloop+1
            
            
    #find sload state variable, struct, array, mapping
    #find the key                    
    for j in range(0,len(b)):
        sstoreindex=b.iloc[j,0].find('SSTORE')  
        if (sstoreindex>0):   
            storesplit=re.split(r'(?:[, : \s])',b.iloc[j,0])
            if (len(storesplit)>8):
                storekey=storesplit[7]
                staddressindex=storekey.find('(')
                if(staddressindex>0):  ##find state variable, struct, array
                    storeaddress=storekey[(staddressindex+1):]
                    storeaddressmodify=storekey[:(len(storeaddress)-1)]
                    store_var='stor_'+storeaddressmodify
                    #print([b.iloc[j,1],store_var]) #modify here
                    SD_edge.append([store_var, b.iloc[j,1], b.iloc[j,3]])
                else:
                    leftfind=[j]
                    uloop=1
                    findSHA3=0
                    while(findSHA3<1 and uloop<10):
                        findSHA3=0
                        SHAsplit=[]
                        for m in range(0,len(leftfind)):
                            SHAsplit=list(set(SHAsplit+re.split(r'(?:[,])',b.iloc[leftfind[m],3])))
                        #print('SHAsplit',SHAsplit)
                        leftfind=[]
                        for n in range(0,len(SHAsplit)):
                            if (SHAsplit[n]!='0' and b.iloc[:,2].tolist().count(SHAsplit[n])>0):
                                 leftfind.append(b.iloc[:,2].tolist().index(SHAsplit[n]))
                                 #print('leftfind',leftfind)
                        for m in range(0,len(leftfind)):
                            if (b.iloc[leftfind[m],4].find('SHA3')<0):
                                findSHA3=findSHA3 or 0
                            if (b.iloc[leftfind[m],4].find('SHA3')>-1):
                                findSHA3=findSHA3 or 1
                                #print(leftfind[m])
                                if(b.iloc[leftfind[m],0].count('(')>0 and b.iloc[leftfind[m],0].count(')')>0):
                                    SHAaddress1=b.iloc[leftfind[m],0][b.iloc[leftfind[m],0].index('(')+1:b.iloc[leftfind[m],0].index(')')]
                                if(b.iloc[leftfind[m],0].count(')')>0):
                                    delete=b.iloc[leftfind[m],0][b.iloc[leftfind[m],0].index(')')+1:]    
                                if(b.iloc[leftfind[m],0].count('(')>0 and b.iloc[leftfind[m],0].count(')')>0 and delete.count('(')>0 and delete.count(')')>0):
                                    SHAaddress2=delete[delete.index('(')+1:delete.index(')')]
                                    mapping='stor_'+SHAaddress1+'_'+SHAaddress2
                                    #print([b.iloc[j,1],mapping]) ##modify here
                                    SD_edge.append([mapping, b.iloc[j,1], b.iloc[j,3]])
                        uloop=uloop+1
    return SD_edge




def forwardPropagate(G, taint_nodes):
    k=0 
    next_hop = taint_nodes
    last_hop = taint_nodes          
    while(len(next_hop)>0 and k<100):
        next_nodes=[] 
        next_hop = []
        for i in range(0,len(last_hop)):
            if (last_hop[i] in G):
                next_nodes=list(G.successors(last_hop[i]))
            #print(next_nodes)
            next_hop= next_hop + next_nodes
        taint_nodes=taint_nodes + next_hop
        last_hop=next_hop
        k=k+1
    return list(set(taint_nodes))

#G=nx.DiGraph()
#G.add_edge('A','B')
#G.add_edge('B','D')
#G.add_edge('B','C')

#taint_nodes=forwardPropagate(G, ["A"])
#print(taint_nodes)


def dataflow_propagate(vul_variable, dataflow_edge):
    taint_op_list=['ADD','MUL','SUB','DIV','SDIV','MOD','SMOD','EXP','NOT','LT','GT','SLT','SGT','EQ','ISZERO','SIGNEXTEND','AND','OR','XOR','BYTE','SHL','SHR','SAR','ADDMOD','MULMOD','ADDRESS','BALANCE','CALLER','CALLVALUE','CALLDATALOAD','CALLDATACOPY','RETURNDATACOPY','POP','MLOAD','MSTORE','MSTORE8','SLOAD','SSTORE']
    taint_DFG=nx.DiGraph()
    for n in range (0, len(dataflow_edge)):
        if (dataflow_edge[n][2] in taint_op_list):
            taint_DFG.add_edge(dataflow_edge[n][0], dataflow_edge[n][1])
    vul_variable=forwardPropagate (taint_DFG, vul_variable)
    return list(set(vul_variable))


def controlflow_propagate(vul_block, CFG):
    vul_block=forwardPropagate (CFG, vul_block)
    return vul_block

def getvulnervariable (b, vulnerable_functions):
    vulval=[]
    for m in range (0, len(vulnerable_functions) ):
        for n in range(0,len(b)):
            if (b.iloc[n,5]==vulnerable_functions[m] and b.iloc[n,0].find("function")<0):
                right_split=re.split(r'(?:[ , ])',b.iloc[n,3])
                if(len(right_split)==3 and right_split[1]!='0' and right_split[2]!='0'):
                    vulval.append(right_split[1])
                    vulval.append(right_split[2])
                if(len(right_split)==2 and right_split[1]!='0'):
                    vulval.append(right_split[1])
                if (b.iloc[n,2]!='0'):
                    vulval.append(b.iloc[n,2])
                
    return list(set(vulval))


def vulnerabilitydetction(path, vulnerable_functions):
    [b, graph_index]=generate_ListandGraph (path)
    vulval=getvulnervariable (b, vulnerable_functions)
    #print ("vulval",vulval)
    dataflow_edge = DFG_edge(b)
    vul_variable = dataflow_propagate(vulval, dataflow_edge)
    #print("vul_variable",vul_variable)
    statevariable=find_statevariable (path,b)
    #CFG = CFGgeneration (path) 
    #vul_block = controlflow_propagate(["0x21f4B0xf1a"], CFG)
    taint_stor=[]
    for i in range (0, len(statevariable)):
        for j in range (0, len(vul_variable)):
            if (statevariable[i][2].find(vul_variable[j])>0):
                taint_stor.append(statevariable[i][0])
    return list(set(taint_stor))

with open('vulnerability_analysis_results.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # 写入CSV表头
    #writer.writerow(['合约名', '漏洞函数', '漏洞函数数量', '被污染的存储变量数量'])
    
    # 写入数据
    current_dir = os.getcwd()

    for file in os.listdir(os.path.join(current_dir, '.temp')):

        start_time=time.time()
        vulnerable_functions=[]
        all_library=[]
        taint_stor=[]
        if os.path.exists(os.path.join(current_dir, 'detect-library', file + '.txt')):
            with open(os.path.join(current_dir, 'detect-library', file + '.txt'),'r') as f:
                all_line=f.readlines()
            for line in all_line:
                if line.strip()!='':
                    line=line.strip().split(' ')
                    if line[1].split('\'')[1] not in vulnerable_functions:
                        vulnerable_functions.append(line[1].split('\'')[1])
                    if line[0].split('\'')[1] not in all_library:
                        all_library.append(line[0].split('\'')[1])
            path = os.path.join(current_dir, '.temp', file, 'out')
            taint_stor=vulnerabilitydetction(path, vulnerable_functions)
        end_time=time.time()
        
        # 格式化漏洞函数列表为字符串
        vul_func_str = '; '.join(vulnerable_functions) if vulnerable_functions else '无'
        vul_func_count = len(vulnerable_functions)
        tainted_storage_count = len(taint_stor)
        
        print(f"分析完成: {file} - 漏洞函数数量: {vul_func_count}, 被污染存储变量数量: {tainted_storage_count}")
        writer.writerow([file, vul_func_str, vul_func_count, tainted_storage_count])  # 写入数据行




#python3 vul-detectionviataintanalysis.py