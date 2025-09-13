import os,shutil
def transfer_newdasm():
    for file in os.listdir('./preprocess/dasm'):
        with open('./preprocess/dasm/'+file,'r') as f:
            all_newline=''
            all_lines=f.readlines()
            for line in all_lines:
                newline=line.strip(' ')
                newline=newline.split(' ')
                all_newline+=newline[0]+' '
                all_newline+=newline[1]
                if '\n' not in newline[1]:
                    all_newline+='\n'
            with open('./preprocess/new_dasm/'+file,'w') as f2:
                f2.write(all_newline[:-1])

def tran_temp():
    for contract_dir in os.listdir('./.temp'):
        if os.path.exists('./.temp/'+contract_dir+'/contract.dasm'):
            shutil.copy('./.temp/'+contract_dir+'/contract.dasm','./preprocess/dasm/'+contract_dir+'.dasm')
        if os.path.exists('./.temp/'+contract_dir+'/out/contract.tac'):
            shutil.copy('./.temp/'+contract_dir+'/out/contract.tac','./all_contract_tac/'+contract_dir+'.tac')
def data():
    with open('./Statement_Opcode.facts','r') as sta:
        new_dict={}
        all_stalines=sta.readlines()

        for line in all_stalines:
            line.strip()
            line=line.split(' ')
            new_dict[line[1].strip()]=line[0].strip()
        for file in os.listdir('./preprocess/new_dasm'):
            with open('./preprocess/new_dasm/'+file,'r') as f:
                new_bytecode_line=''
                new_data_line=''
                all_lines=f.readlines()
                for line in all_lines:
                    newline=line.split(' ')[1].strip()
                    if newline!='MISSING':
                        new_bytecode_line+=new_dict[newline][2:]
                        new_data_line+=new_dict[newline][2:]+' '
                with open('./preprocess/new_bytecode/'+file,'w') as f2:
                    f2.write(new_bytecode_line)
                with open('./preprocess/data/'+file,'w') as f3:
                    f3.write(new_data_line)       

         
def train_data():
    for file in os.listdir('./preprocess/data'):

        print(file)
        with open('./preprocess/data/'+file,'r') as f:
            new_bytecode_line=''
            new_data_line=''
            no_log_dasm=''
            all_instruc=f.readline().strip().split(' ')
            with open('./preprocess/new_dasm/'+file) as new_dasm:
                exist_log_line=new_dasm.readlines()
            with open('./preprocess/dasm/'+file,'r') as dasm:
                dasm_line=dasm.readlines()
                i=0
                j=0
                while i < len(dasm_line):
                    if 'MISSING' in dasm_line[i]:
                        i=i+1
                        continue
                    if 'PUSH31    0x11e9e55e13c0f9f7ea956f4b1e8ba65ba63e88d7c306b9d90b9564cdd30c11' in dasm_line[i]:
                        if all_instruc[j]=='7e' and ((j+9)<len(all_instruc) and all_instruc[j+9]=='a1') and all_instruc[j+1]=='60' and all_instruc[j+2]=='51' and all_instruc[j+5]=='80':            
                            i=i+10
                            j=j+10
                            if 'PUSH31    0x22c74b3a86ea8dfa255116234c1bcddd89a3f4379935fa263daefeb087008e' in dasm_line[i]:
                                if all_instruc[j]=='7e' and ((j+9)<len(all_instruc) and all_instruc[j+9]=='a1') and all_instruc[j+1]=='60' and all_instruc[j+2]=='51' and all_instruc[j+5]=='80':       
                                    i=i+10
                                    j=j+10
                                    continue
                            no_log_dasm+=exist_log_line[i]
                            new_bytecode_line+=all_instruc[j]+' '
                            new_data_line+='S '
                    elif 'PUSH31    0x22c74b3a86ea8dfa255116234c1bcddd89a3f4379935fa263daefeb087008e' in dasm_line[i]:
                        if all_instruc[j]=='7e' and ((j+9)<len(all_instruc) and all_instruc[j+9]=='a1') and all_instruc[j+1]=='60' and all_instruc[j+2]=='51' and all_instruc[j+5]=='80':       
                            new_data_line=new_data_line[:-2]
                            new_data_line+='E '            
                            i=i+10
                            j=j+10
                        
                    else:
                        no_log_dasm+=exist_log_line[i]
                        new_bytecode_line+=all_instruc[j]+' '
                        new_data_line+='N '
                        i=i+1
                        j=j+1
                with open('./preprocess/true_data/'+file,'w') as f2:
                    f2.write(new_bytecode_line)
                with open('./preprocess/true_label/'+file,'w') as f3:
                    f3.write(new_data_line)
                with open('./preprocess/no_log_dasm/'+file,'w') as f4:
                    f4.write(no_log_dasm)
                    
def main():
    tran_temp()
    transfer_newdasm()
    data()
    train_data()
if __name__ == '__main__':
    main()



