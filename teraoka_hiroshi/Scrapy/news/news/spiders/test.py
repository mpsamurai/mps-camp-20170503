#スクレイピング
import scrapy
class SpiderName(scrapy.Spider):
    #name = 'yahoo'
    name = 'yahoonews'
    #start_urls = ['yahoo.co.jp',]
    start_urls = ['https://news.yahoo.co.jp',]  #変数名は決まって入る
    #https: // news.yahoo.co.jp /
#    def parse(self, response):
#        #data = response.css('a::text').extract()
#        ##data = response.css('div[id=epTabTop] a::text').extract()  #div(class='epTabTop')内の<a>タグのtextを取得
#        data = response.css('div[id=subMod subRanking] span::text').extract()
#        print(data)
#        yield data




        # 通常データベースをOpenしたりcloseしたりはロス
        # アイテムがきたら sussor開いてcusserとじる

        # プログラムを入れるようにテーブルを作ってDBへデータを入れる
        # class PileLine:
        #   def open_spider(self, spider):
        #   //データベースへの接続
        #
        #   def process_item(self, item, spider):
        #   //アイテムのデータベースへの登録  (corsorはとじたり引いたりはOK)
        #       return item
        #
        #   def close_spider(self, spider):
        #       //データベースへの接続解除 (DBは開いたりとじるりはロスなので)
        #
        #

#########課題
# ニュースヘッドライン(タイトル)　と　カテゴリ(組)を取得する
#ニュースのカテゴライスをしたい
#ライターに好きな記事を書いてもらって
#メールをもらい
#記事のタイトルをスクレイプしてカテゴリごとに振り分けたい

#ヘッドライン自体を見つける
#そのカテゴリがどこから得られるか調べる(ページ内)
#見つけたらそのHTML構造はどうなっていて特徴を調査して
#CSSセレクタを使って取得する


#yahoo newsのカテゴリ３つだけでも１０万とれる