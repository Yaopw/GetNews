
from django_echarts.entities import (
    Copyright, ValuesPanel, ValueItem, NamedCharts, WidgetCollection,
    bootstrap_table_class, RowContainer
)
from django_echarts.starter import DJESite, SiteOpts
from django_echarts.stores.entity_factory import factory
from pyecharts import options as opts
from pyecharts.charts import Bar,Pie
from pyecharts.charts import Bar
from pyecharts import options as opts
import pandas as pd
import sys
sys.path.append('../../')
print(sys.path)
from collections import Counter
import pickle

with open('data/doc_sentiment.pkl', 'rb') as f:
    doc_sentiment = pickle.load(f)
with open('data/transposed_lst.pkl', 'rb') as f:
    transposed_lst = pickle.load(f)
with open('data/word_freq_5.pkl', 'rb') as f:
    word_freq_5 = pickle.load(f)
with open('data/word_freq_4.pkl', 'rb') as f:
    word_freq_4 = pickle.load(f)
with open('data/word_freq_3.pkl', 'rb') as f:
    word_freq_3 = pickle.load(f)
with open('data/topic_lst.pkl', 'rb') as f:
    topic_lst = pickle.load(f)
with open('data/lda_model.pkl', 'rb') as f:
    lda_model = pickle.load(f)
with open('data/corpus.pkl', 'rb') as f:
    corpus = pickle.load(f)
with open('data/dictionary.pkl', 'rb') as f:
    dictionary = pickle.load(f)
__all__ = ['site_obj']

site_obj = DJESite(
    site_title='百度热点新闻内容分析系统',
    opts=SiteOpts(list_layout='list')
)

site_obj.add_widgets(
    copyright_=Copyright(start_year=2022, powered_by='Zinc'),
    # jumbotron=Jumbotron('福建统计', main_text='数据来源：福建统计局', small_text='2022年2月'),
    values_panel='home1_panel',
    # jumbotron_chart='search_word_cloud'
)



# 绘制饼图
@site_obj.register_chart(title='文档级情感分类',
                         description='文档级情感分类（4类）饼图',
                         catalog='基本图表',top=1)
def test1():

    dd = Counter(doc_sentiment)
    dict1={'star 5':'非常积极','star 4':'积极','star 3':'中性','star 2':'消极','star 1':'非常消极',}
    def func1(x):
        return dict1[x]
    labels = list(dd.keys())
    sizes = list(dd.values())
    labels=map(func1,labels)
    pie = Pie()
    pie.add("", [list(z) for z in zip(labels, sizes)], radius=["30%", "70%"],
            label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    pie.set_global_opts(title_opts=opts.TitleOpts(title="文档各情感极性所占比例"))
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    return pie
@site_obj.register_chart(title='句子级情感分类',
                         description='句子级情感分类（3类）柱状图',
                         catalog='基本图表',top=2)
def test2():

    labels = ['文章1', '文章2', '文章3', '文章4']
    data1 = transposed_lst[0]
    data2 = transposed_lst[1]
    data3 = transposed_lst[2]
    bar = (
        Bar()
        .add_xaxis(labels)
        .add_yaxis('无情感', data1)
        .add_yaxis('消极', data2)
        .add_yaxis('积极', data3)
        .set_global_opts(title_opts=opts.TitleOpts(title='四篇文章中各情感极性数量'))
    )
    return bar


from pyecharts import charts
@site_obj.register_chart(title='情感极性为非常积极的文章词云图',
                         description='情感极性为非常积极的文章词云图',
                     catalog='词云图')

def test3():
    word_cloud = (
        charts.WordCloud()
        .add(series_name="情感极性为非常积极的文章词云图", data_pair=list(word_freq_5.items()))
        .set_global_opts(title_opts=opts.TitleOpts(title="情感极性为非常积极的文章词云图"))
    )
    return word_cloud
@site_obj.register_chart(title='情感极性为较积极的文章词云图',
                         description='情感极性为较积极的文章词云图',
                         catalog='词云图')
def test4():
    word_cloud = (
        charts.WordCloud()
        .add(series_name="情感极性为较积极的文章词云图", data_pair=list(word_freq_4.items()))
        .set_global_opts(title_opts=opts.TitleOpts(title="情感极性为较积极的文章词云图"))
    )
    return word_cloud
@site_obj.register_chart(title='情感极性为中性的文章词云图',
                         description='情感极性为中性的文章词云图',
                         catalog='词云图')
def test5():
    word_cloud = (
        charts.WordCloud()
        .add(series_name="情感极性为中性的文章词云图", data_pair=list(word_freq_3.items()))
        .set_global_opts(title_opts=opts.TitleOpts(title="情感极性为中性的文章词云图"))
    )
    return word_cloud

@site_obj.register_chart(title='新闻题材分析',
                         description='新闻题材（政治、经济、科教、军事、社会、文艺、体育）所占比例饼图',
                         catalog='基本图表',top=6)
def test6():

    dd = Counter(topic_lst)
    labels = list(dd.keys())
    sizes = list(dd.values())
    pie = Pie()
    pie.add("", [list(z) for z in zip(labels, sizes)], radius=["30%", "70%"],
            label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    pie.set_global_opts(title_opts=opts.TitleOpts(title="新闻主题所占比例"))
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    return pie




@site_obj.register_html_widget
def home1_panel():
    number_p = ValuesPanel()
    number_p.add_widget(ValueItem('100', '最近新闻数', '条'))
    number_p.add(str(factory.chart_info_manager.count()), '图表总数', '个', catalog='danger')
    # number_p.add('42142', '网站访问量', '人次')

    # number_p.add('8.0', '福建省2021年GDP增长率', '%', catalog='info')
    # number_p.add('89.00', '中国联通5G套餐费用', '元', catalog='success')
    number_p.set_spans(6)
    return number_p

