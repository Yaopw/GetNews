#!/usr/bin/env python
# coding: utf-8

import numpy as np
import re
import string
import jieba
from transformers import pipeline
import snownlp
from collections import Counter
import glob
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))

import pprint
pprint.pprint(sys.path)
def read_txt_files(folder_path):
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    txt_contents = []
    for txt_file in txt_files:
        with open(txt_file, 'r',encoding='utf-8') as f:
            txt_content = f.read()
        txt_contents.append(txt_content)
    return txt_contents

folder_path = '../scrapy/newsArticle'
txt_contents = read_txt_files(folder_path)


stop_lst=['文章','标题','链接']
with open('../data/cn_stopwords.txt',encoding='utf-8') as f:
    for line in f.readlines():
        stop_lst.append(line.strip('\n'))
        
punc = string.punctuation + u'.,;《》？！“”‘’@#￥%…&×（）——+【】{};；●，。&～、|\s:：'

def clean(text):
    text = text.lower()
    text = ''.join([re.sub(r"[{}]+".format(punc), '', s) for s in text])
    text = re.sub(r'[0-9]', ' ', text)
    text = re.sub(r'[a-z]', ' ', text)
    text=' '.join(text.split())
    return text.strip('')
def fcut1(text):
    text=clean(text)
    return " ".join(jieba.cut(text, cut_all=False))
def fcut2(text):
    text=clean(text)
    return "".join(jieba.cut(text, cut_all=False))

lst=list(map(fcut1,txt_contents))
lst0=list(map(fcut2,txt_contents))
lst1=[i[:500] for i in lst0]
model = pipeline('sentiment-analysis',model='techthiyanes/chinese_sentiment')
lst2=model(lst1)
doc_sentiment=[i['label'] for i in lst2]
def get_doc_sentiment():
    return doc_sentiment


def get_transposed_lst():
    def sent_func(x):
        if x>0.8:
            return 2
        elif x<0.2:
            return 1
        else:
            return 0
    sent_lst=[]
    i_lst=[]
    for i in range(len(txt_contents)):
        text =txt_contents[i]
        if len(text)<1000:
            continue
        sentence = snownlp.SnowNLP(text).sentences
        sent_sentiment=[snownlp.SnowNLP(i).sentiments for i in sentence]
        C=Counter(list(map(sent_func,sent_sentiment)))
        sent_lst.append([C[0],C[1],C[2]])
        i_lst.append(i)
        if len(i_lst)>=4:
            break
    arr = np.array(sent_lst)
    transposed_lst = np.transpose(arr).tolist()
    return transposed_lst

def get_word_freq():
    lst3,lst4,lst5=[],[],[]
    for i,sent in enumerate(doc_sentiment):
        if sent=='star 5':
            lst5.append(i)
        elif sent=='star 4':
            lst4.append(i)
        else:
            lst3.append(i)    
    text=''
    for i in lst5:
        text+=lst[i]
    words = [w for w in jieba.cut(text) if w not in stop_lst and w!=' ']
    word_freq_5 = {}
    for word in words:
        if word in word_freq_5:
            word_freq_5[word] += 1
        else:
            word_freq_5[word] = 1
            
    text=''
    for i in lst4:
        text+=lst[i]
    words = [w for w in jieba.cut(text) if w not in stop_lst and w!=' ']
    word_freq_4 = {}
    for word in words:
        if word in word_freq_4:
            word_freq_4[word] += 1
        else:
            word_freq_4[word] = 1
            
    text=''
    for i in lst3:
        text+=lst[i]
    words = [w for w in jieba.cut(text) if w not in stop_lst and w!=' ']
    word_freq_3 = {}
    for word in words:
        if word in word_freq_3:
            word_freq_3[word] += 1
        else:
            word_freq_3[word] = 1  
    return word_freq_5,word_freq_4,word_freq_3

doc_sentiment=get_doc_sentiment()
transposed_lst=get_transposed_lst()
word_freq_5,word_freq_4,word_freq_3=get_word_freq()
import pickle
with open('data/doc_sentiment.pkl', 'wb') as f:
    pickle.dump(doc_sentiment, f)
with open('data/transposed_lst.pkl', 'wb') as f:
    pickle.dump(transposed_lst, f)
with open('data/word_freq_5.pkl', 'wb') as f:
    pickle.dump(word_freq_5, f)
with open('data/word_freq_4.pkl', 'wb') as f:
    pickle.dump(word_freq_4, f)
with open('data/word_freq_3.pkl', 'wb') as f:
    pickle.dump(word_freq_3, f)