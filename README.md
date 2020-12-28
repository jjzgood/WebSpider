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

