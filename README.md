# WebSpider

## 介绍
爬虫的一些测试用例和学习的代码。

```python
# 创建项目
scrapy startproject tutorial
# 创建Spider
cd tutorial
scrapy genspider quotes quotes.toscrape.com
# 运行spider
scrapy crawl quotes
```

###  1. tutorial： 初学spider的第一个入门例子。

- 了解spider工作的简单流程

*  spider保存到数据库

### 2. scrapydownloadertest：中间件的用法

* 修改request agent
* 修改response status

### 3. images360：ItemPipelines的用法

* 保存爬取的图片到本地
* 保存相关信息到mongodb
* 保存相关信息到mysql

### 4. bilibili：爬取bilibili up的视频信息，并根据标题生成云图

### 5. cloudword：生成云图代码

### 6. scrapypyppeteer：动态页面爬取和分布式爬虫









