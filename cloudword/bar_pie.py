import pymongo
import re
from collections import defaultdict
import matplotlib.pyplot as plt


class Figure:
    """
    画饼图和柱形图
    """
    def __init__(self,key,value):
        self.key = key
        self.value = value
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

    def plt_pie(self,title):
        plt.figure(figsize=(10, 8.5))
        plt.pie(self.value, labels=self.key, autopct='%1.1f%%')
        plt.title(title)
        plt.savefig(title+'.png')
        plt.show()

    def plt_bar(self,title):
        plt.figure(figsize=(10, 8.5))
        plt.bar(self.key, self.value)
        plt.title(title)
        plt.xlabel('主播名字或者节目名')
        plt.ylabel('播放量(万)')
        # x轴旋转
        plt.xticks(rotation=-60)
        # 设置数字标签
        for a,b in zip(self.key,self.value):
            plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'bottom',fontsize=10)
        plt.savefig(title+'.png')
        plt.show()


host = 'localhost'
port = 27017
db = 'uploader'
collection = 'guanchazhe'

client = pymongo.MongoClient(host=host, port=port)
db = client[db]
collection = db[collection]
result = collection.find()

play_counts = defaultdict(int)
for item in result:
    title = item['title']
    if item['play'] == '--':
        continue
    if re.search('骁话一下',title):
        play_counts['骁话一下'] += item['play']
    elif re.search('逸语道破',title):
        play_counts['逸语道破'] += item['play']
    elif re.search('懂点儿啥',title):
        play_counts['懂点儿啥'] += item['play']
    elif re.search('排雷小分队|以理扶人',title):
        play_counts['排雷小分队和以理扶人'] += item['play']
    elif re.search('施佬胡诌',title):
        play_counts['施佬胡诌'] += item['play']
    elif re.search('亚洲特快',title):
        play_counts['亚洲特快'] += item['play']
    elif re.search('这个我慧',title):
        play_counts['这个我慧'] += item['play']
    elif re.search('新之说',title):
        play_counts['新之说'] += item['play']
    elif re.search('洋媒吐气',title):
        play_counts['洋媒吐气'] += item['play']
    else:
        play_counts['其他'] += item['play']


play_counts_sort = sorted(play_counts.items(),key=lambda item:item[1],reverse=True)
play_key = [key[0] for key in play_counts_sort]
play_value = [key[1]/10000 for key in play_counts_sort]

figure = Figure(play_key[1:],play_value[1:])
figure.plt_pie('观察者主播播放量百分比')
figure.plt_bar('观察者主播播放量柱形图')