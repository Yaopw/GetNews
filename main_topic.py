#!/usr/bin/env python
# coding: utf-8

import re
import string
import jieba
from transformers import pipeline
from collections import Counter
from pyecharts import options as opts
import os
import glob
import tqdm
import pickle

def read_txt_files(folder_path):
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    txt_contents = []
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as f:
            txt_content = f.read()
        txt_contents.append(txt_content)
    try:
        txt_contents1=txt_contents[-100:]
    except:
        txt_contents1=txt_contents
    return txt_contents1


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
    pattern = r'http\S+|www\S+'
    text=re.sub(pattern, '', text)
    return text.strip('')
def fcut1(text):
    text=clean(text)
    return " ".join(jieba.cut(text, cut_all=False))
def fcut2(text):
    text=clean(text)
    return "".join(jieba.cut(text, cut_all=False))

txt_contents=map(clean,txt_contents)

processed_data = []
for text in txt_contents:
    words = [word for word in list(jieba.cut(text)) if word not in stop_lst]
    processed_data.append(''.join(words))
txt_contents=processed_data


model = pipeline('zero-shot-classification',model='morit/chinese_xlm_xnli')


res_lst=[]
cat_lst=['政治：指与政治体系相关的事物，例如政府机构、政治活动、政治事件、政策和政治思想等。政治在社会中起着至关重要的作用，它涉及到权力、组织、管理、决策和社会规范等多个方面。'
,'经济：指与经济体系相关的事物，例如经济活动、商业、财务、市场和货币等。经济是社会发展的重要基础，它涉及到生产、分配、交换和消费等多个方面。'
,'科教：指与科学技术和教育相关的事物，例如科研、技术发展、教育制度、学校和教育政策等。科技和教育是社会发展和进步的关键因素，它们涉及到知识、智力、技能和人才等多个方面。'
,'军事：指与国防和军事力量相关的事物，例如军队、武器装备、军事行动、军事技术和军事战略等。军事是维护国家安全和领土完整的重要手段，它涉及到战争、防御、威慑和战略等多个方面。'
,'社会：指与社会生活和社会问题相关的事物，例如社会组织、社会文化、社会福利、社会调查和社会问题等。社会是人类生活的基本单位，它涉及到人际关系、文化传承、价值观念和社会结构等多个方面。'
,'体育：指与体育运动和体育文化相关的事物，例如体育赛事、运动员、体育产业、健身和休闲等。体育是人类健康和快乐生活的重要组成部分，它涉及到身体健康、运动技能和团队合作等多个方面。']
for txt in tqdm.tqdm(txt_contents):
    if len(txt)>500:
        txt=txt[:500]
    res=model(txt,candidate_labels=cat_lst)['labels'][0][:2]
    res_lst.append(res)


with open('data/topic_lst.pkl', 'wb') as f:
    pickle.dump(res_lst, f)



import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
import jieba
from gensim import corpora, models

texts = []
for text in txt_contents:
    lst=jieba.lcut(text)
    lst1=[]
    for i in lst:
        try:
            if len(i)>=2:
                lst1.append(i)
            else:
                continue
        except:
            continue
    texts.append(lst1)
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
lda_model = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=4)


import pickle
with open('data/lda_model.pkl', 'wb') as f:
    pickle.dump(lda_model, f)
with open('data/corpus.pkl', 'wb') as f:
    pickle.dump(corpus, f)
with open('data/dictionary.pkl', 'wb') as f:
    pickle.dump(dictionary, f)



vis = gensimvis.prepare(lda_model, corpus, dictionary)
pyLDAvis.save_html(vis, 'templates/lda.html')


data_dir = '../scrapy/newsArticle'
news_list=[]
for file_name in os.listdir(data_dir):
    with open(os.path.join(data_dir, file_name), 'r', encoding='utf-8') as f:
        content = f.read()
        news_list.append(content)


