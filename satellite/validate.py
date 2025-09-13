import os ,shutil,ast,json,pdb
import difflib
def process_block(line):
    line_num=line.strip().split('0x')[1]
    if line_num.endswith('B'):
        line_num=line_num[:-1]
    return line_num,''


def process_colon(line):
    line_num=line.strip().split(':')[0].split('0x')[1]
    line_signature=''
    line=line.strip().split(' ')
    if 'MLOAD' in line  :
        line_signature='A'
    elif  'SLOAD' in line:
        line_signature='B'
    elif 'MSTORE' in line :
        line_signature='C'
    elif  'SSTORE' in line:
        line_signature='D'
    elif 'JUMP' in line :
        line_signature='E'
    elif  'JUMPI' in line:
        line_signature='F'
    elif  'JUMPDEST' in line:
        line_signature='G'
    elif  'CALLPRIVATE' in line:
        line_signature='H'
    elif  'STATICCALL' in line:
        line_signature='I'
    elif  'DELEGATECALL' in line:
        line_signature='J'
    elif  'CALL' in line:
        line_signature='K'
    elif  'CALLVALUE' in line:
        line_signature='L'
    elif 'CALLER'  in line   :
        line_signature='M'
    elif  'CALLDATALOAD' in line:
        line_signature='N'
    elif  'CALLDATASIZE' in line:
        line_signature='O'
    elif  'CALLDATACOPY' in line:
        line_signature='P'
    elif  'CALLCODE' in line:
        line_signature='Q'
    elif 'LT'  in line :
        line_signature='R'
    elif  'GT' in line:
        line_signature='S'
    elif  'SLT' in line:
        line_signature='T'
    elif  'SGT' in line:
        line_signature='U'
    elif  'EQ' in line:
        line_signature='V'
    elif  'ISZERO' in line:
        line_signature='W'
    elif 'RETURN'  in line:
        line_signature='X'
    elif  'RETURNDATASIZE' in line:
        line_signature='Y'
    elif  'RETURNDATACOPY' in line:
        line_signature='Z'
    elif 'REVERT' in line:
        line_signature='0'
    elif 'GASPRICE'  in line:
        line_signature='1'
    elif 'GASLIMIT' in line:
        line_signature='2'
    elif 'GAS' in line:
        line_signature='3'
    elif 'LOG' in line:
        line_signature='4'
    elif  'SHA3' in line:
        line_signature='5'
    elif 'EXTCODESIZE' in line:
        line_signature='6'
    elif 'ADD' in line:
        line_signature='7'
    elif 'DIV' in line:
        line_signature='8'
    elif 'SUB' in line:
        line_signature='9'
    elif 'TIMESTAMP' in line:
        line_signature='a'
    elif 'NUMBER' in line:
        line_signature='b'
    elif 'SELFBALANCE' in line:
        line_signature='c'
    elif 'EXTCODEHASH' in line:
        line_signature='d'
    elif 'ADDRESS' in line:
        line_signature='e'
    elif 'EXTCODECOPY' in line:
        line_signature='f'
    return line_num,line_signature    

def count_unique_characters(s):
    # 创建一个集合，将字符串中的所有字符添加进去
    unique_chars = set(s)
    
    # 返回集合的长度，即字符种类的个数
    return len(unique_chars)
def process_function(all_line):
    function_name=all_line.split('(')[0].split(' ')[1]
    return function_name
def process_lines(all_line):
    num=[]
    signature=[]
    function_num=[]
    function_name=[]
    line_no=0
    while line_no <len(all_line):
        if '0x11e9e55e13c0f9f7ea956f4b1e8ba65ba63e88d7c306b9d90b9564cdd30c11' in all_line[line_no]:
            i=0
            while i<7:
                return_num, return_signature=process_colon(all_line[line_no+i])
                num.append(return_num)
                signature.append('')
                i+=1
            line_no+=7
        elif '0x22c74b3a86ea8dfa255116234c1bcddd89a3f4379935fa263daefeb087008e' in all_line[line_no]:
            i=0
            while i<7:
                return_num, return_signature=process_colon(all_line[line_no+i])
                num.append(return_num)
                signature.append('')
                i+=1
            line_no+=7
        elif 'Begin block' in all_line[line_no]:
            return_num, return_signature=process_block(all_line[line_no])
            num.append(return_num)
            signature.append(return_signature)
            line_no+=1
        elif ':' in all_line[line_no]:
            return_num, return_signature=process_colon(all_line[line_no])
            num.append(return_num)
            signature.append(return_signature)
            line_no+=1
        elif 'function' in all_line[line_no]:
            return_name=process_function(all_line[line_no])
            return_num,_=process_block(all_line[line_no+1])
            function_num.append(return_num)
            function_name.append(return_name)
            line_no+=1
        else:
            line_no+=1
    return num,signature,function_num,function_name

def signature(path):
    with open(path,'r') as f:
        all_line=f.readlines()
    num,signature,function_num,function_name=process_lines(all_line)
    return num ,signature,function_num,function_name

def open_predict_dasm(path):
    with open(path,'r') as f:
        all_line=f.readlines()
    return all_line

def open_func_predict(path):
    with open(path,'r') as f:
        all_line=f.readlines()
    func_list = ast.literal_eval(all_line[0].strip())
    return func_list

def predict_function_location(func_list,all_line):
    all_line_num=[]
    func_num_enum=[]
    for line in all_line:
        all_line_num.append(line.strip().split(':')[0].split('0x')[1])
    for func_enum in func_list:
        func_num_enum.append((all_line_num[func_enum[0]],all_line_num[func_enum[1]]))
    return func_num_enum

def find_function(list1,num):
    i=0
    while i+1 <len(list1):
        if num>list1[i] and num<list1[i+1]:
            return i
        i+=1
    return i

def predict_function_signature(file_num,file_signture,func_num_enum,function_num,function_name):
    all_func_signature=[]
    func_index=[]
    all_func_name=[]
    num=0
    while num <len(function_num):
        func_index.append(file_num.index(function_num[num]))
        num+=1
    for func_bound in func_num_enum:
        start=func_bound[0]
        end=func_bound[1]
        func_signature=''
        if start in file_num:
            start_index=file_num.index(start)
        else:
            while start not in file_num:
                start=hex(int(start,16)-1)[2:]
            start_index=file_num.index(start)
        if end in file_num:
            end_index=file_num.index(end)
        else:
            while end not in file_num:
                end=hex(int(end,16)+1)[2:]            
            end_index=file_num.index(end)
        for i in range(start_index,end_index+1):
            func_signature+=file_signture[i]
        all_func_name.append(function_name[find_function(func_index,start_index)])
        all_func_signature.append(func_signature)
    return all_func_signature,all_func_name

def longest_common_substring(str1, str2):
    dp = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]

    # 最长子串的长度
    max_length = 0

    # 遍历二维数组，填充dp数组
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                max_length = max(max_length, dp[i][j])
            else:
                dp[i][j] = 0  # 如果不匹配，则当前位置设为0

    return max_length

def validate(all_vul_list,all_func_signature,all_func_name):
    flag=False
    all_match_name=[]
    for func_signature in all_func_signature:
        for vul in all_vul_list:
            #if func_signature == vul :
            min_lenth=len(vul)
            len_min=min_lenth
            if min_lenth>20:
                min_lenth=20
                len_1=longest_common_substring(func_signature,vul)
                if len_1>=min_lenth:
                    if count_unique_characters(vul)+3>count_unique_characters(func_signature) and count_unique_characters(func_signature)+3>count_unique_characters(vul):
                     
                        if len(vul)<1.3*len(func_signature) and len(func_signature) <1.3*len(vul):
                            flag=True
                            
                            all_match_name.append(all_func_name[all_func_signature.index(func_signature)])
            else:
                if func_signature[:min_lenth]==vul[:min_lenth] or func_signature[1:min_lenth+1]==vul[:min_lenth] or func_signature[2:min_lenth+2]==vul[:min_lenth]:
                    if count_unique_characters(vul)+2>count_unique_characters(func_signature) and count_unique_characters(func_signature)+2>count_unique_characters(vul):
                        if len(vul)<1.8*len(func_signature) and 0.5*len(func_signature) <len(vul):
                            flag=True
           
    return flag ,all_match_name

def process_real_vulnerabilities():
    """处理真实漏洞：读取vul目录，生成签名，更新vul_signature.json"""
    current_dir = os.getcwd()
    vul_dir = os.path.join(current_dir, 'vul')
    vul_signature_path = os.path.join(current_dir, 'vul_signature.json')
    dasmpath = os.path.join(current_dir, 'preprocess', 'no_log_dasm')
    tacpath = os.path.join(current_dir, 'all_contract_tac')
    
    # 读取现有的漏洞签名
    if os.path.exists(vul_signature_path):
        with open(vul_signature_path, 'r') as f:
            all_vul_dict = json.load(f)
    else:
        all_vul_dict = {}
    
    new_signatures_added = 0
    
    if not os.path.exists(vul_dir):
        print("vul目录不存在，跳过真实漏洞处理")
        return all_vul_dict, new_signatures_added
    
    print("开始处理真实漏洞...")
    
    for vul_file in os.listdir(vul_dir):
        if vul_file.endswith('.txt'):
            contract_name = vul_file[:-4]  # 去除.txt后缀
            vul_file_path = os.path.join(vul_dir, vul_file)
            
            # 读取真实漏洞边界
            try:
                with open(vul_file_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        real_bounds = ast.literal_eval(content)
                    else:
                        continue
            except Exception as e:
                print(f"读取漏洞文件 {vul_file} 失败: {e}")
                continue
            
            if not real_bounds:
                continue
            
            print(f"处理合约 {contract_name} 的真实漏洞边界: {real_bounds}")
            
            # 查找对应的TAC和DASM文件
            tac_file = os.path.join(tacpath, contract_name + '.tac')
            dasm_file = os.path.join(dasmpath, contract_name + '.dasm')
            
            if not os.path.exists(tac_file) or not os.path.exists(dasm_file):
                print(f"  找不到对应的TAC或DASM文件，跳过")
                continue
            
            try:
                # 生成文件签名
                file_num, file_signature, function_num, function_name = signature(tac_file)
                all_line = open_predict_dasm(dasm_file)
                
                # 将真实边界转换为地址边界
                func_num_enum = predict_function_location(real_bounds, all_line)
                
                # 生成真实漏洞函数的签名
                real_vul_signatures, real_func_names = predict_function_signature(
                    file_num, file_signature, func_num_enum, function_num, function_name
                )
                
                print(f"  生成的真实漏洞签名: {real_vul_signatures}")
                
                # 检查并添加新签名到漏洞库
                if contract_name not in all_vul_dict:
                    all_vul_dict[contract_name] = []
                
                for vul_sig in real_vul_signatures:
                    if vul_sig not in all_vul_dict[contract_name]:
                        all_vul_dict[contract_name].append(vul_sig)
                        new_signatures_added += 1
                        print(f"  添加新漏洞签名: {vul_sig}")
                    else:
                        print(f"  签名已存在: {vul_sig}")
                        
            except Exception as e:
                print(f"处理合约 {contract_name} 时出错: {e}")
                continue
    
    # 保存更新后的漏洞签名库
    if new_signatures_added > 0:
        with open(vul_signature_path, 'w') as f:
            json.dump(all_vul_dict, f, indent=2)
        print(f"已添加 {new_signatures_added} 个新漏洞签名到 vul_signature.json")
    else:
        print("没有新的漏洞签名需要添加")
    
    return all_vul_dict, new_signatures_added

def main():
    current_dir = os.getcwd()
    dasmpath = os.path.join(current_dir, 'preprocess', 'no_log_dasm')
    tacpath = os.path.join(current_dir, 'all_contract_tac')
    predictpath = os.path.join(current_dir, 'predict')
    vul_path = os.path.join(current_dir, 'vul_signature.json')
    dstpath = os.path.join(current_dir, 'detect-library')
    
    # 确保输出目录存在
    os.makedirs(dstpath, exist_ok=True)
    
    # 第一步：处理真实漏洞，生成并更新漏洞签名库
    all_vul_dict, new_signatures_added = process_real_vulnerabilities()
    
    print("\n" + "="*50)
    print("开始验证预测结果...")
    
    # 第二步：进行预测验证
    for file in os.listdir(tacpath):
        print(f"验证文件: {file}")
        dasmfile = os.path.join(dasmpath, file[:-4]+'.dasm')
        tacfile = os.path.join(tacpath, file)
        predictfile = os.path.join(predictpath, file[:-4]+'.txt')
        storepath = os.path.join(dstpath, file[:-4]+'.txt')
        
        # 检查必要文件是否存在
        if not os.path.exists(dasmfile) or not os.path.exists(predictfile):
            print(f"  跳过 {file}: 缺少必要文件")
            continue

        try:
            file_num, file_signature, function_num, function_name = signature(tacfile)
            all_line = open_predict_dasm(dasmfile)
            func_list = open_func_predict(predictfile)
            func_num_enum = predict_function_location(func_list, all_line)
            all_func_signature, all_func_name = predict_function_signature(
                file_num, file_signature, func_num_enum, function_num, function_name
            )
            
            #print(f"  预测函数签名: {all_func_signature}")
            
            vul_list = []
            for key in all_vul_dict:
                exist, func_names = validate(all_vul_dict[key], all_func_signature, all_func_name)
                if exist:
                    for name in func_names:
                        if (key, name) not in vul_list:
                            vul_list.append((key, name))
            
            # 保存检测结果
            with open(storepath, 'w') as f:
                for li in vul_list:
                    f.write(f'{li}\n')
            
            if vul_list:
                print(f"  ✓ 检测到漏洞: {vul_list}")
            else:
                print(f"  - 未检测到漏洞")
                
        except Exception as e:
            print(f"  处理文件 {file} 时出错: {e}")
            continue

    print("\n验证完成!")
    print(f"本次新增漏洞签名: {new_signatures_added}")
    print(f"检测结果保存在: {dstpath}")

if __name__ == '__main__':
    main()