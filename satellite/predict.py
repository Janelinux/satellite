'''
from fairseq.models.roberta import RobertaModel
import os
from collections import defaultdict
from colorama import Fore, Back, Style
import torch
import sys
roberta = RobertaModel.from_pretrained('checkpoints/funcbound', 'checkpoint_best.pt',
                                       'data-bin/funcbound', bpe=None, user_dir='finetune_tasks')
roberta.eval()
all_label=[]
with open('./data-raw/sol_funcbound/true.txt','r') as f:  
    with open('./data-raw/predict/test.txt','w') as f2:
        
        all_line=f.readlines()
        all_token=all_line[0].strip().split(' ')
        for i in range(0,len(all_token),510):
            if i+512>=len(all_token):
                encoded_tokens = roberta.encode(' '.join(all_token[i:len(all_token)]))
            else:
                encoded_tokens = roberta.encode(' '.join(all_token[i:i+510]))
            logprobs = roberta.predict('funcbound', encoded_tokens)
            labels = logprobs.argmax(dim=2).view(-1).data
            for i_token, label in enumerate(labels):
                if label==0:
                    f2.write(all_token[i+i_token]+' -\n')
                elif label==1:
                    f2.write(all_token[i+i_token]+' E\n')
                elif label==2:
                    f2.write(all_token[i+i_token]+' S\n')
            for i, (token, label) in enumerate(zip(all_token, labels)):
                if label == 0:
                    print(f'{token}', end=" ")
                elif label == 2:
                    print(f'{Fore.RED}{token}{Fore.RESET}', end=" ")
                elif label == 1:
                    print(f'{Fore.GREEN}{token}{Fore.RESET}', end=" ")
'''

import os
os.chdir('./XDA')
os.system('python3 predict.py')
os.chdir('../')

