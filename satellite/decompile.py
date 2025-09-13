import os
import time
data_path=os.getcwd()
contract_path=f'{data_path}/bytecode/'
k1=0
all_file=[]
for file in os.listdir('./.temp'):
        all_file.append(file)


for file_name in os.listdir(data_path + "/bytecode"):

        #if file_name[:-4] in all_file:
        #        continue
        k1+=1 
       
        os.system("python3 ./gigahorse/gigahorse-toolchain/gigahorse.py -C ./gigahorse/gigahorse-toolchain/clients/visualizeout.py '" + data_path + "/bytecode/"+file_name+"'")
       
