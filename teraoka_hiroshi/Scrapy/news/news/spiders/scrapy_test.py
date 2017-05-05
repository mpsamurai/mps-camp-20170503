import scrapy

#Yahoo Newsのトピックニュースタイトルをスクレイピング
# TODO
#  |--リファクタリングをする
#  |--


class SpiderName(scrapy.Spider):
    name = 'yahoo_news'
    start_urls = ['https://news.yahoo.co.jp/list/?c=sports']

    def parse(self, response):
        next_page = 1
        item = {}
        categorydata = response.css('span[class=supple] span[class=cate]::text').extract() #ページ内のカテゴリ名
        itemdata = response.css('div[class=listArea] span[class=ttl]::text').extract() #ページ内のニュースフィードタイトルを抽出する
        for i,d in zip(categorydata,itemdata):
            item[d] = i
        yield item

        next_page = response.css('li[class=next] a::attr(href)').extract()
        #次のページを取得したら
        if next_page: #有る限り(次のページ)


            next_page = response.urljoin(next_page[0])  # responseはフレームワークでurlが定義されてる

            yield scrapy.Request(url=next_page)


