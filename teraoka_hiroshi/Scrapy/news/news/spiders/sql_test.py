# SQL について
# システムのインフラを作る人たちは重要だけど
# アプリケーションを作る側の人たちには今はそこまで考えなくても大丈夫なようになってきている

# データベース作成
# (db) # create database database_name owner dbowner_name;
#
# データベースを消す
# > drop database  (name);
# データベース接続
# $ psql -d postgres
# => \l                              (データベース一覧の表示)
# => \c データベース名   (データベースの選択して起動)
# => \dt;                           (テーブル一覧の表示)
# => \d テーブル名;          (テーブル構造の表示)
# => select * from テーブル名; (テーブル内のデータを一覧)
#
#


# PATH
# export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin
#
#
#
#
#

import psycopg2


try: #ドライバでDBとのパイプを作ってくれて入る
    conn = psycopg2.connect("dbname='pycamp_20170503'user='pycamp' host='localhost'password='pycamp'")
except:
    print('unable to connect')


# カーソルを使ってsql文実行
cur = conn.cursor()   # １本のパイプでDB用の処理を走らせるが、その中に細い線を作ってsql文を書き込む
# create tableでテーブル作成しましょう
# cur.execute('create table emails(id serial primary key, text_body text, html_body text, sender varchar);')

# conn.commit()  #cur.executeはgit add と同じ状態で commitして初めてDBに上がる

# cur.close()

# conn.close()

# DB に　接続確認
# > \c pycamp_20170503
# > \dt テーブル一覧
# > select * from table_name; これでテーブルが見れる

# プレイスホルダー式
# cur. #insert into とはnewsの中にvalueを入れろよ
# cur.execute("insert into emails(text_body, html_body, sender) values(%s,%s,%s);", ('text','html','sender'))
# conn.commit()
# sql文に操作する時、プレイスホルダーで操作すること
#
#
# primary keyとは テーブルを取得するために serial(連続した) primary key を用意しておくこと

cur.execute("insert into emails(text_body, html_body, sender) values(%s,%s,%s);", ('text','html','sender'))

conn.commit()

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
#
#
#