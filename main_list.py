#!/usr/bin/env python
# coding: utf-8
import re
import os
import glob
import pickle
from transformers import pipeline
import snownlp

def read_txt_files(folder_path):
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    txt_contents = []
    for txt_file in txt_files:
        with open(txt_file, 'r',encoding='utf-8') as f:
            txt_content = f.read()
        txt_contents.append(txt_content)
    txt_contents1=txt_contents[-100:]
    return txt_contents1

folder_path = '../scrapy/newsArticle'
txt_contents = read_txt_files(folder_path)

def get_url(text):
    url_pattern = re.compile(r'https?://\S+')
    match = url_pattern.search(text)
    if match:
        return match.group(0)
    else:
        return None


def get_title(text):
    start_str = '文章标题：'
    end_str = '\n'
    start_idx = text.index(start_str) + len(start_str)
    end_idx = text.index(end_str, start_idx)
    result = text[start_idx:end_idx]
    return result

def get_content(text):
    start_str = '文章标题：'
    end_str = '\n'
    start_idx = text.index(start_str) + len(start_str)
    end_idx = text.index(end_str, start_idx)
    result = text[end_idx+1:]
    return result


link_lst=[get_url(i) for i in txt_contents]
title_lst=[get_title(i) for i in txt_contents]
content_lst=[get_content(i) for i in txt_contents]

print('正在生成摘要')
summarizer = pipeline('summarization',model='yihsuan/mt5_chinese_small')
res_lst=summarizer(content_lst,max_length=500)


summary_lst=[i['summary_text'] for i in res_lst]


keywords_lst=[]
for text in content_lst:
    try:
        s = snownlp.SnowNLP(text)
        keywords = s.keywords(limit=5)
        keywords_lst.append(str(keywords))
    except:
        keywords_lst.append('无')


with open('data/link_lst.pkl', 'wb') as f:
    pickle.dump(link_lst, f)
with open('data/title_lst.pkl', 'wb') as f:
    pickle.dump(title_lst, f)
with open('data/content_lst.pkl', 'wb') as f:
    pickle.dump(content_lst, f)
with open('data/summary_lst.pkl', 'wb') as f:
    pickle.dump(summary_lst, f)
with open('data/keywords_lst.pkl', 'wb') as f:
    pickle.dump(keywords_lst, f)
