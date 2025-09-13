import os
import time
data_path='/pro/decom/XDA'
contract_path='/pro/decom/XDA/bytecode/'
k1=0
#decompilation
#decompilation
for file_name in os.listdir(data_path + "/bytecode"):
        k1+=1      
        #decompilation
        os.system("mkdir datasetoutput")
        print(k1,file_name)
        print(data_path + "/bytecode")
        os.system("docker start gig")
        
        os.system("python3 ./gigahorse/gigahorse-toolchain/gigahorse.py -C ./gigahorse/gigahorse-toolchain/clients/visualizeout.py '" + data_path + "/bytecode/"+file_name+"'")
        os.system("docker cp  '"+ data_path + "/bytecode/"+file_name+"' gig:/home/reviewer/demo.hex")
        os.system("timeout 20s docker exec gig bash -c \"/home/reviewer/gigahorse-toolchain/bin/generatefacts /home/reviewer/demo.hex out && /home/reviewer/gigahorse-toolchain/decompiler_compiled --facts out\"")

        for file in os.listdir(data_path+"/.temp/"+file_name[:-4]+"/out"):
                os.system("docker cp  '"+data_path+"/.temp/"+file_name[:-4]+"/out/"+file+"' gig:/home/reviewer/gigahorse-toolchain/logic")
        os.system("timeout 20s docker exec gig bash -c \"/home/reviewer/gigahorse-clients/source_decompiler.dl_compiled\"")
        os.system("timeout 20s docker exec gig bash -c \"/home/reviewer/gigahorse-clients/get_source.py\"")
        os.system("docker cp gig:/home/reviewer/gigahorse-toolchain/logic "+data_path+"/datasetoutput")
        for file2 in os.listdir(data_path+"/datasetoutput/logic"):
                os.system("cp -fr "+data_path+"/datasetoutput/logic/"+file2+" '"+data_path+"/.temp/"+file_name[:-4]+"/out'")
        os.system("docker exec gig bash -c \"rm -rf /home/reviewer/gigahorse-toolchain/logic\"")

        os.system("docker stop gig")
        for file in os.listdir(data_path+"/.temp/"+file_name[:-4]):
                if file=="out":
                        for file2 in os.listdir(data_path+"/.temp/"+file_name[:-4]+"/out"):
                                if file2=="decompiled.sol":
                                
                                        os.chdir(data_path+"/.temp/"+file_name[:-4]+"/out")
                                        os.system("mv decompiled.sol '"+file_name[:-4]+".sol'")
                                        os.chdir(data_path)
                        
        os.system("rm -rf datasetoutput")
        
        
#python3 generate.py
#python3 ./gigahorse/gigahorse-toolchain/gigahorse.py -C ./gigahorse/gigahorse-toolchain/clients/visualizeout.py /pro/decom/cross-chain-bugs/experiment/new/QBridge2.0.hex