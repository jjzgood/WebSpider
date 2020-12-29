import pymongo
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt


class GenWordImage:
    """
    生成词云
    """
    def __init__(self,host,port,db,collection,bgimage,save_name):
        """
        :param host: mongo地址
        :param port: 端口
        :param db:
        :param collection:
        :param bgimage: 生成图片的背景图
        :param save_name: 生成的图片保存的名称
        """
        self.host = host
        self.port = port
        self.db = db
        self.collection = collection
        self.bgimage = bgimage
        self.save_name = save_name
        self.stopword = self.stopwords('ChineseStopWords.txt')

    def mongo_data(self):
        client = pymongo.MongoClient(host=self.host,port=self.port)
        db = client[self.db]
        collection = db[self.collection]
        return collection.find()

    def stopwords(self,file='ChineseStopWords.txt'):
        stopword = set()
        with open(file,encoding='utf-8') as f:
            for line in f:
                stopword.add(line.rstrip('\r\n'))
        return stopword

    def handle_data(self):
        words = {}
        for item in self.mongo_data():
            title = item['title']
            # description = item['description']
            # text = title + description
            text = title
            for word in jieba.cut(text):
                if word not in self.stopword:
                    words[word] = words.get(word, 0) + 1
        total = len(words)
        frenq = {k: v / total for k, v in words.items()}
        return frenq

    def gen_image(self,show=False):
        """
        :param show: 是否显示图片
        """
        wc = WordCloud(
            font_path='simhei.ttf',  # 字体路劲
            background_color='white',  # 背景颜色
            width=1000,
            height=600,
            max_font_size=80,  # 字体大小
            min_font_size=10,
            mask=plt.imread(self.bgimage),  # 背景图片
            max_words=1000
        )
        wc.fit_words(self.handle_data())
        # 图片保存
        wc.to_file(self.save_name+'.png')
        if show:
            # 显示图片
            plt.figure(self.collection)  # 图片显示的名字
            plt.imshow(wc)
            plt.axis('off')  # 关闭坐标
            plt.show()


if __name__ == '__main__':
    task = GenWordImage(
        host='localhost',
        port=27017,
        db='uploader',
        collection='chineseboy',
        bgimage = 'images/heart.jpg',
        save_name='chineseboy'
    )
    task.gen_image()




