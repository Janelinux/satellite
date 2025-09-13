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
import numpy as np
from fairseq.models.roberta import RobertaModel
import os

# Translate predictions to code offsets
def translate_predictions(starts, ends):
    # Pair starts/ends to create function bounds
    bounds = []

    if len(starts) == 0 or len(ends) == 0:
        return bounds
    label_list=[]
    combined_list=sorted(starts+ends)
    for num in combined_list:
        if num in starts:
            label_list.append('S')
        elif num in ends:
            label_list.append('E')
    label_num=0
    while label_num+1<len(label_list):
        if label_list[label_num]=='S' and label_list[label_num+1]=='E':
            bounds.append((combined_list[label_num],combined_list[label_num+1]))
        label_num+=1

   
    return bounds


def eval_bound_predictions(pred_bounds, real_bounds):
    # Build confusion matrix
    cm = np.zeros((2, 2), dtype=int)

    i, j = 0, 0

    while i < len(pred_bounds) and j < len(real_bounds):

        # True positive
        if pred_bounds[i][0] == real_bounds[j][0] and pred_bounds[i][1] == real_bounds[j][1]:
            cm[0, 0] += 1
            i += 1
            j += 1

        # False positive
        elif pred_bounds[i][0] < real_bounds[j][0]:
            cm[0, 1] += 1
            i += 1

        # False negative
        else:
            cm[1, 0] += 1
            j += 1

    while i < len(pred_bounds):
        cm[0, 1] += 1
        i += 1

    while j < len(real_bounds):
        cm[1, 0] += 1
        j += 1

    precision = cm[0, 0] / (cm[0, 0] + cm[0, 1])
    recall = cm[0, 0] / (cm[0, 0] + cm[1, 0])
    f1 = 2 * (precision * recall) / (precision + recall)

    print("F1: {:.6f}, Precision: {:.6f}, Recall: {:.6f}".format(f1, precision, recall))
    print(cm)

    return cm


def eval_bound_predictions1(pred_bounds, real_bounds):
    pred_bounds_set = set(pred_bounds)
    real_bounds_set = set(real_bounds)

    TP = pred_bounds_set & real_bounds_set
    p = len(TP) / len(pred_bounds_set)
    r = len(TP) / len(real_bounds_set)
    print(f"F1: {2 * (p * r) / (p + r)}, Precision: {p}, Recall: {r}")


def predict(filename, model):
    f_truth = open(f'../preprocess/true_data/{filename}', 'r')
    f_label=open(f'../preprocess/true_label/{filename}', 'r')

    starts_label = []
    ends_label = []
    starts_pred = []
    ends_pred = []

    tokens = []
    '''
    for i, line_truth in enumerate(f_truth):
        # if i > 10000:
        #     break

        line_truth_split = line_truth.strip().split(' ')
        tokens.append(line_truth_split[0].lower())
        if len(line_truth_split) > 1:
            # if line_truth_split[1] == 'F':
            if line_truth_split[1] == 'S':
                starts_label.append(i)
            # elif line_truth_split[1] == 'R':
            elif line_truth_split[1] == 'E':
                ends_label.append(i)
            else:
                pass
    f_truth.close()
    '''
    all_line=f_truth.readlines()
    all_label=f_label.readlines()
    f_truth.close()
    f_label.close()
    tokens=all_line[0].strip().split(' ')
    true_labels=all_label[0].strip().split(' ')
    for i ,label in enumerate(true_labels):
        if label=='S':
            starts_label.append(i)
        elif label=='E':
            ends_label.append(i)
    for i_block in range(0, len(tokens), 510):
        if i_block + 510 > len(tokens):
            to_encode_tokens = tokens[i_block:len(tokens)]
        else:
            to_encode_tokens = tokens[i_block:i_block + 510]

        encoded_tokens = model.encode(' '.join(to_encode_tokens))
        logprobs = model.predict('funcbound', encoded_tokens[:510])
        labels = logprobs.argmax(dim=2).view(-1).data

        for i_token, label in enumerate(labels):
            if label == 2:
                starts_pred.append(i_block + i_token)
            elif label == 1:
                ends_pred.append(i_block + i_token)
    return starts_label, ends_label, starts_pred, ends_pred


# Load our model
roberta = RobertaModel.from_pretrained('checkpoints/funcbound', 'checkpoint_best.pt',
                                       'data-bin/funcbound', bpe=None,
                                       user_dir='finetune_tasks')
roberta.eval()
k=0
for file in os.listdir('../preprocess/true_data'):
    
    print(file)
    starts_label, ends_label, starts_pred, ends_pred = predict(
        file, roberta)
    #print(starts_pred)
    #print(ends_pred)

    #print(starts_label)
    #print(ends_label)
    bounds_label = translate_predictions(starts_label, ends_label)
    #print(bounds_label)

    bounds_pred = translate_predictions(starts_pred, ends_pred)
    with open('../predict/'+file[:-5]+'.txt','w') as f:
        f.writelines(str(bounds_pred))
    #print(bounds_pred)
    #eval_bound_predictions(bounds_pred, bounds_label)
    k+=1
