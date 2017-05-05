# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2


class NewsPipeline(object):
    def process_item(self, item, spider):
        return item



class PileLine:
    def __init__(self):



        self.conn = psycopg2.connect("dbname='pycamp_20170503'user='pycamp' host='localhost'password='pycamp'")

    def open_spider(self, spider):
        ##以下cur文２行は１回やれば二回以降はコメントアウト
        cur = self.conn.cursor()
        cur.execute('create table news(id serial primary key, category text, newstitle varchar);')

        self.conn.commit()

        return self

    def process_item(self, item, spider):
        # アイテムのデータベースへの登録
        print('item_len', len(item))

        cur = self.conn.cursor()
        for key,value in item.items():
            # print(value)
            cur.execute("insert into news(category, newstitle) values(%s,%s);", (value, key))

        self.conn.commit()

        cur.close()
        return item

    def close_spider(self, spiders):
        self.conn.close()
