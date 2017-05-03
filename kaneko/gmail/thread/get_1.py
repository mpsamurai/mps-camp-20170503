import base64
import httplib2
import oauth2client
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage



SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = '/Users/hiroshiteraoka/GW/secrets/client_id.json'
APPLICATION_NAME = 'pycamp-20170503_1'

store = Storage('/Users/hiroshiteraoka/GW/secrets/gmail.json')
credentials = store.get()
if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES) #Client_secret(身分書)を使って認証して!条件も伝える
    credentials = tools.run_flow(flow, store) #上記手順を実行させる(結果,証明書がくれば=>credentialsに入れてくれ)

http = credentials.authorize(httplib2.Http()) #クレデンシャルをもったらgoogleへ投げて見てよの手順
service = discovery.build('gmail', 'v1', http=http) #実際にgoogleにアクセスする機能の塊を作る

response = service.users().threads().list(userId='me').execute() #塊(service)をgoogleへ投げる users().threads()スレッドが文章の塊をリストでください(これはjsonで戻る)
threads = response.get('threads', [])

#使用として#######################
# ①threadsをリストで取得するメソッド
# ②リストから要素を取得するメソッド
# ③要素(jsonファイル)をcsvファイルに保存するメソッド
#まずは以上をお客様へだせる状態にする
################################


#次のページを取ってくる
#if 'threads' in response:
#    threads.extend(response['threads'])
#めちゃくちゃ多いから回数指定

#ダウンロードはアクセスリミットもあるので
#回数を指定する要素が必要
n = 0
while 'nextPageToken' in response:
    print(response['threads'])
    if n < 5:
        page_token = response['nextPageToken']
        response = service.users().threads().list(userId='me',pageToken=page_token).execute()
        threads.extend(response['threads'])
        n += 1
    else:
        break


# 以下もらったjson形式を解析
###if not threads: #大元のスレッド
###    print('No threads found.')
###else:
###    for thread in threads:
###        print('id:', thread['id'])
#    thread = service.users().threads().get(userId='me', id=threads[0]['id']).execute() #usersの中のスレッドを抜き出し、持ち主は私、指定したidを抜き出す
#    message = ''
#    for part in thread['messages'][0]['payload']['partId']: #jsonはディクショナリなのでmessagesのなかのpayloadのなかのpartsで
#        message += base64.urlsafe_b64decode(part['body']['data']).decode() #body内のdataをデコードして取り出す
#    print(message)


import csv
#def csv_get(threads):

    # 以下もらったjson形式を解析
if not threads: #大元のスレッド
    print('No threads found.')
else:
    for thread in threads:
        print('id:', thread['id'])

    with open('threads.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerows([[thread['id'],]])


#開発のフローになれる
#Gitのコミットをこまめにやること
##git commit 0m "  "
# 自分の作業履歴になるし、戻れるためのセーブみたいなものだし、チームでもこまめにやると助かる
#関数を作りました-> git commit -m "関数〜作りました"
# git commit -m "引数◯を追加しました"
# git commit -m "●◯のバグを解決"
# git commit -m "リファクタリング●◯を●◯の構造に変更"
# これをほとんどやってないと仕事していないことと同じ(イス座ってただけ)
#####ここまでは自分のローカル上のPCで動いて入るだけ。
####
# こんな悪いコミットはダメ！以下
# git commit -m "コミット" 意味わからない


#git add されたあとの話
# git mv source(ファイル名) dest(フォルダ名) #とするとadd済みファイルが自分の環境に移動する
# git rm ファイル名 #add済みファイルを消せる

#####
#動くようになったなと思ったらリモート(GitHubなど)へ送って成果物を報告
# git push origin master
###
## pushしたら、GitHubページに行ってPullリクエストして(ボタン押して)終了
#このプルリクエストはgit commit の頻度では送るな！多すぎるからね,(これでいいのかな!?)
#　pullリクエストしてから質問する



####Gitの話
# コミット間違えた!
# git reset --soft ^Head (直前のコミット履歴のみ消せる:コミットだけ間違えた!場合)
# git reset --hard ^Head (直前のコミット履歴と編集ファイルのコードを削除されるので、もう全て消したい！場合のみ)


## .gitignoreファイルとは
#無視するフォルダやファイルを指定するものです
# ここに書いてあるフォルダ,ファイルは add されないし無視される
# ここには絶対にアップロードしたくないファイルなどを書いておく
# ここは正規表現使える
# 例えば、テストデータファイルは出したくない **/test や
# バックアップファイル(test.py~) などをださないために *~ とする

#####慣れてくるとブランチを切る

