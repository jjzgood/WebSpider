from scrapy import Item,Field


class UploaderItem(Item):
    # bv id
    bvid = Field()
    title = Field()
    description = Field()
    # 播放
    play = Field()
    # 评论
    comment = Field()
    # 创建时间
    created = Field()