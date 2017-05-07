#スクレイピング
import scrapy
class SpiderName(scrapy.Spider):
    name = 'yahoo_news1'
    start_urls = ['https://news.yahoo.co.jp/list/?c=sports'] #　スポーツカテゴリ
    def parse(self, response):
        #data = response.css('ul[class=cateTab] a::text').extract()
        data = response.css('div[class=backnumber] ul[class=cateTab] a::text').extract()
        #data = response.css('div[class=backnumber] ul[class=cateTab] ul[class=list] span[class=ttl]::text').extract()
        print(data)
        yield data

        #次のページを取得したら
        #if next_page:





#yahoo newsのカテゴリ３つだけでも１０万とれる


# for url in self.start_urls:
# response = self._get_response(rul)
# for data in self.parse(response):
#     if isinstance(data,(scrapy.Request型)):
#     else:
#         データを処理するプログラム

#     response = self.get_response(url)
#     item = self.parse(response) #ここでparse()関数へ投げて帰って来るものをitemへだけど一連の流れが終わったら次のページを取得
#        以下へ
# ジェネレータ
#
# class SpiderName(scrapy.Spider): #Spiderベースクラスを継承 あとは問題依存を定義する
#   name = 'spider name'
#   start_urls = ['url1,','url2'...] #パースするためにページ情報をURLで指定して中身をしゅとくするその後responseに投げる
#
#   def parse(self, response):  #spiderで情報を取ってきてくれるとこまで自動でしてくれるその戻り値にresponseに入って来る
#         yield data  #responseの中身のデータをここで解析する

#       if next_page:
#             yield scrapy.Request(url=next_page_url) #next_page_urlを取得してくるもの、データを詰め込んだオブジェクトを持って入る

