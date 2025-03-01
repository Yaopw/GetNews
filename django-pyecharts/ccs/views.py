from typing import Any

from django_echarts.entities import (
    Container, RowContainer, ValuesPanel, Title
)
from django_echarts.stores.entity_factory import factory
from django_echarts.views import PageTemplateView
from django.shortcuts import render
from django.http import HttpResponse
from .models import News
import os
import signal
import pickle
import subprocess
class LDA(PageTemplateView):
    template_name = 'lda.html'


with open('data/link_lst.pkl', 'rb') as f:
    link_lst = pickle.load(f)
with open('data/title_lst.pkl', 'rb') as f:
    title_lst = pickle.load(f)
with open('data/content_lst.pkl', 'rb') as f:
    content_lst = pickle.load(f)
with open('data/summary_lst.pkl', 'rb') as f:
    summary_lst = pickle.load(f)
with open('data/keywords_lst.pkl', 'rb') as f:
    keywords_lst = pickle.load(f)
with open('data/doc_sentiment.pkl', 'rb') as f:
    doc_sentiment = pickle.load(f)
with open('data/topic_lst.pkl', 'rb') as f:
    topic_lst = pickle.load(f)


def run_scripts(request):
    running = False
    if request.method == 'POST':
        print('正在运行')
        # request.POST['running'] = 'True'
        running = True
    subprocess.call(['python', '../scrapy/spider_news.py'])
    subprocess.call(['python', '../main_sentiment.py'])
    subprocess.call(['python', '../main_topic.py'])
    subprocess.call(['python', '../main_list.py'])
    return render(request, 'run_scripts.html',{'running': running})
def news_list(request):
    news_list1 = []
    for i in range(len(title_lst)):
        news = News(title=title_lst[i],content=content_lst[i],link=link_lst[i],ids=i,)
        news_list1.append(news)
    return render(request, 'news_list.html', {'news_list': news_list1})

def news_detail(request, news_id):
    # 获取指定ID的新闻对象
    news = News(title=title_lst[news_id],content=content_lst[news_id],
                link=link_lst[news_id],summary=summary_lst[news_id],
                keywords=keywords_lst[news_id],sentiment=doc_sentiment[news_id],
                topic=topic_lst[news_id],
                ids=news_id)
    # 渲染新闻详情页面
    return render(request, 'news_detail.html', {'news': news})