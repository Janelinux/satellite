def process_line(all_line):
    for line in all_line:
        if 'prev=[' in line:
            continue
        elif 'Begin block' in line:
        elif ':' in line:
            
        else:
            continue
def signature(path):
    with open(path,'r') as f:
        all_line=f.readlines()
    