import MeCab
import psycopg2
from gensim import corpora, models, similarities

import csv
#test = "半年で休み４日「過労死」残業が国の上限未満でも認定"
#tagger = MeCab.Tagger("-Owakati")
#result = tagger.parse(test)
#print(result)

# 文章の類似度計算をしたい
# 今回はニュースのヘッドラインの集まり
# ヘッドラインとして、「コンピューター」「経済」「国際」などそれぞれカテゴリを用意
# これから新しく取ってきた文章を

try: #ドライバでDBとのパイプを作ってくれて入る
    conn = psycopg2.connect("dbname='pycamp_20170503'user='pycamp' host='localhost'password='pycamp'")
except:
    print('unable to connect')



cur = conn.cursor()
types = ['スポーツ','エンタメ','IT']
dictionarys = {}
documents = {'スポーツ':[],'エンタメ':[],'IT':[]}
tagger = MeCab.Tagger("-Owakati")
corpus = {}
tfitf = {}
for type in types:

    # select * from テーブル名 where カラム名(欲しい先) like %s;", (スポーツカテゴリ,))
    cur.execute("select * from yahoonews where category like %s;",(type,))
    # cur.executeはデータベースのテーブル１番目に紐づいた(値は取ってこない)
    # 取りたいなら data = cur.fetchone() な感じ
    row = cur.fetchone()
    headline = row[2] if row else None


    while headline:

        #print(title)

        headline = tagger.parse(headline).split(' ')
        # typeは今,['スポーツ','エンタメ','IT']がfor type in typesで入れられて入る
        documents[type].append(headline) # あるカテゴリのヘッドラインを集めて入る

        row = cur.fetchone()
        headline = row[2] if row else None


    dictionary = corpora.Dictionary(documents[type])


    # ベクトル化[0,1,0,0..0,0,0,1]         [textヘッドライン] [カテゴリごと集合のヘッドライン]
    corpus[type] = [dictionary.doc2bow(text) for text in documents[type]]
    #print(corpus) # corpusは辞書でできている

    # for corpus_test in corpus[type]:
    #    corpus_test = corpus_test
    #    print(corpus_test)

    # tfitf = models.TfidfModel(corpus_test)
    # print(tfitf)
    #  http://tawara.hatenablog.com/entry/2016/11/08/021408
    # Error -> 'int'object is not iterable(intオブジェクトは反復不能)エラーがでる
    #tfitf[type] = [models.TfidfModel(corpus_test) for corpus_test in corpus[type]]

# corpus[type]には辞書型が作られていて、typeのキーに対応した値が[]配列文字で入っている
# それを抜き出しながら tfitf[type]のキーに対応させながら値を[]配列文字で入れたい
    #print('tfitf========',tfitf)
    tfitf[type] = models.TfidfModel(corpus[type])  # corpus[type]で作ったデータをそのまま入れればよかっただけ.
    test = 'メッシへの処分解除＝代表戦の出場可能に―FIFA'
    tagger.parse(test)
    vec = dictionary.doc2bow(test.split(' '))
    print(tfitf[type])
    print(tfitf[type][vec])  # tfitf[type]カテゴリーの[vec]配列をみる
    # シミラリティ（類似度)はもう１ステップ

    # コーパスのTF-IDFモデルの実装

# TF: Term Frequency
#
# ある単語が元の文章にどれくらい現れるのか？
# ある単語が元の文章になんども現れるようなら重要な単語だろう

# IF-IDF:
# でも、回数は違っても希少性がある単語

# 希少性も頻発性も合わせたものをTF-IDFモデル