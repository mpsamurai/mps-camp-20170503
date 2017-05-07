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

#仕様として#######################
# ①threadsをリストで取得するメソッド
# ②threadsの「次のページ」を取得する
# ③listから要素(jsonファイル)をcsvファイルに保存するメソッド
#まずは以上をお客様へだせる状態にする
################################


###①「threadsをlistを取得する」################
def list_get(store, SCOPES, CLIENT_SECRET_FILE):
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES) #Client_secret(身分書)を使って認証して!条件も伝える
        credentials = tools.run_flow(flow, store) #上記手順を実行させる(結果,証明書がくれば=>credentialsに入れてくれ)

    http = credentials.authorize(httplib2.Http()) #クレデンシャルをもったらgoogleへ投げて見てよの手順
    service = discovery.build('gmail', 'v1', http=http) #実際にgoogleにアクセスする機能の塊を作る

    response = service.users().threads().list(userId='me').execute() #塊(service)をgoogleへ投げる users().threads()スレッドが文章の塊をリストでください(これはjsonで戻る)
    threads = response.get('threads', [])

    return response, threads, service



###②「次のページ」を取ってくる################
#ダウンロードはアクセスリミットもあるので
#回数を指定する要素が必要

#def next_page_get(service, threads):
def next_page_get(func):
    response = func[0]
    threads = func[1]
    service = func[2]
    n = 0
    while 'nextPageToken' in response:
        #print(response['threads'])
        if n < 5:
            page_token = response['nextPageToken']
            response = service.users().threads().list(userId='me',pageToken=page_token).execute()
            threads.extend(response['threads'])
            n += 1
        else:
            break

    return threads



###③listから要素(jsonファイル)をcsvファイルに保存するメソッド################
def csv_get(message):
    import csv
    # def csv_get(threads):
    with open('threads.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        # データをリストに保持
        csvlist = []

        # 以下もらったjson形式を解析
        if not message:  # 大元のスレッド
            print('No threads found.')
        else:
            csvlist.append(message)


        writer.writerows([csvlist,])




############################################
## 簡易テストコード #########
if __name__ == '__main__':
    #googleへ通信しスレッドリスト取得
    thread_list = list_get(store, SCOPES, CLIENT_SECRET_FILE)

    #スレッド１ページ取得後、「次のページ」も取得
    next_page_thread = next_page_get(thread_list)

    #取得されたスレッドをcsvファイルに保存
    csv_file = csv_get(next_page_thread)





##############################
### 拡張を考える ##############
##############################
###今回の処理をテストしてあげる方法を以下に示して入る
###ユーザーが「何をやりたいのか？」を考えて
#class Gmail:
#    def __init__(self, uid):
#        self._threads = []

#    def get_latest(self, title):
#        return None


#class Thread:
#    def __init__(self):
#       self.messages = []


#if __name__ == '__main__':
#    messages = get_messages('me', '2017-1-1') #どんなことがやりたいのか？日付を指定してほしいハズ(メッセージのみ)


#    gmail = Gmail() #Gmailクラスを用意して読み取り専用と最新情報を取得する
#    threads = gmail.get_threads('me', '2017-1-1') #スレッドを取得するのも日付も指定
#    thread = threads.get_latest('mps') #きになるタイトルをいれて送れるようにする
#    for message in thread.messages: #ここで取得したスレッドのメッセージをプリントさせる
#        print(message)
