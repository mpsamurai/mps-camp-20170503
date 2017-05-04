import base64
import httplib2
import oauth2client
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import errors
import json
import base64
import csv
from collections import OrderedDict
from datetime import datetime
import sys
from tqdm import tqdm



__author__ = 'Junya Kaneko <junya@mpsamurai.org>'

def GetThread(service, user_id, thread_id):
    """Get a Thread.
        
        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        thread_id: The ID of the Thread required.
        
        Returns:
        Thread with matching ID.
        """
    try:
        thread = service.users().threads().get(userId=user_id, id=thread_id).execute()
        messages = thread['messages']
        #print ('thread id: %s - number of messages in this thread: %s' % (thread['id'], len(messages)))
        return thread
    except errors.HttpError as error:
        print ('An error occurred: %s' % error )


def ListThreadsWithLabels(service, user_id, label_ids=[]):
    try:
        response = service.users().threads().list(userId=user_id, labelIds=label_ids).execute()
        threads = []
    
        if 'threads' in response:
            threads.extend(response['threads'])
    
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().threads().list(userId=user_id, labelIds=label_ids, pageToken=page_token).execute()
            threads.extend(response['threads'])
    
        return threads
    except errors.HttpError as error:
        print ('An error occurred: %s' % error )


"""Problem:
    Your customer is a company's support center.
    The customer want you to develop a system that sorts their emails on gmail according to those urgency.
    So, you decide to make a words dictionary by using their emails for further analyses.
    Refactor this code so that it can download their all (or at least some) emails from gmail.
    """


SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = '/Users/manzo/Downloads/client_id.json'
APPLICATION_NAME = 'pycamp-20170503'

store = Storage('/Users/manzo/secrets/gmail.json')
credentials = store.get()
if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    credentials = tools.run_flow(flow, store)

http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)


results = ListThreadsWithLabels(service, 'me', label_ids=[])






# keyのリストを取得
ids = [ result['id'] for result in results ]

#HEADERS = ( ("Delivered-To", 0), ("Return-Path", 3), ("Message-ID", 13 ), ("Subject", 17 ), ("From", 18 ), ("To", 19 ), ("Content-Transfer-Encoding", 20 ) )


HEADERS = ( ("Delivered-To", 0), ("Return-Path", 3), ("Message-ID", 13 ), ("Subject", 17 ), ("From", 18 ), ("To", 19 ) )
header_colums = [ title for title, _ in HEADERS ]
header_colums.extend( [ "size", "data", "size", "data" ] )
#header_colums.extend( [ "Content-Transfer-Encoding", "size", "data", "size", "data" ] )

csv_list = [header_colums,]
cnt = 0

#for id in tqdm(ids):
for id in ids:
    print( str(cnt) + ":" + str(id) )
    cnt += 1
    message = GetThread(service, 'me', id)
    #header_body = [ message['messages'][0]['payload']['headers'][val]['value'] for _, val in HEADERS ]
    
    # Setting
    #headers = ( "Delivered-To", "Return-Path", "Message-ID", "Subject","From","To","Content-Transfer-Encoding" )
    headers = ( "Delivered-To", "Return-Path", "Message-ID", "Subject","From","To" )
        
    # initialize
    header_colums = OrderedDict()
        
    for key in headers:
        header_colums[key] = None

    try:

        for header in message['messages'][0]['payload']['headers']:
            if header['name'] in header_colums:
                header_colums[header['name']] = header['value']

            header_body = [ value for _, value in header_colums.items() ]

    except KeyError:
        continue


    """
    for header in message['messages'][0]['payload']['headers']:
        if header['name'] in header_colums:
            header_colums[header['name']] = header['value']
        
        header_body = [ value for _, value in header_colums.items() ]
    """



    if ( "parts" in message['messages'][0]['payload'] ) :
        """
        # Setting
        #headers = ( "Delivered-To", "Return-Path", "Message-ID", "Subject","From","To","Content-Transfer-Encoding" )
        headers = ( "Delivered-To", "Return-Path", "Message-ID", "Subject","From","To" )
        
        # initialize
        header_colums = OrderedDict()

        for key in headers:
            header_colums[key] = None
        """
        # input values
        """""
        for num in len( message['messages'][0]['payload']['headers'] ):
            for key, value in message['messages'][0]['payload']['headers'][num]:
                if key in header_colums:
                    header_colums[key] = value
        """""
        """
        for header in message['messages'][0]['payload']['headers']:
            if header['name'] in header_colums:
                header_colums[header['name']] = header['value']

        line = [ value for _, value in header_colums.items() ]

        
        header_body.extend( line )
        """
        if ( "parts" in message['messages'][0]['payload']['parts'][0] ):
            
            # parts x3
            if ( "parts" in message['messages'][0]['payload']['parts'][0]['parts'][0] ):
                header_body.extend( [
                                     
                                     str( message['messages'][0]['payload']['parts'][0]['body']['size'] ),
                                     base64.urlsafe_b64decode( message['messages'][0]['payload']['parts'][0]['parts'][0]['parts'][0]['body']['data'] ).decode(),
                                     str( message['messages'][0]['sizeEstimate'] ),
                                     base64.urlsafe_b64decode( message['messages'][0]['payload']['parts'][0]['parts'][0]['parts'][1]['body']['data'] ).decode()
                                     ] )
            else:
                # parts x2
                header_body.extend( [
                                 str( message['messages'][0]['payload']['parts'][0]['parts'][0]['body']['size'] ),
                                 base64.urlsafe_b64decode( message['messages'][0]['payload']['parts'][0]['parts'][0]['body']['data'] ).decode(),
                                 str( message['messages'][0]['sizeEstimate'] ),
                                 base64.urlsafe_b64decode( message['messages'][0]['payload']['parts'][0]['parts'][1]['body']['data'] ).decode()
                                 ] )
        
        # parts x1
        else:
            header_body.extend( [
                             str( message['messages'][0]['payload']['parts'][0]['body']['size'] ),
                             base64.urlsafe_b64decode( message['messages'][0]['payload']['parts'][0]['body']['data'] ).decode(),
                             str( message['messages'][0]['sizeEstimate'] ),
                             base64.urlsafe_b64decode( message['messages'][0]['payload']['parts'][0]['body']['data'] ).decode()
                             ] )

    # non parts
    elif ( "headers" in message['messages'][0]['payload'] ):
        header_body.extend( [
                             str( message['messages'][0]['payload']['body']['size'] ),
                             base64.urlsafe_b64decode( message['messages'][0]['payload']['body']['data'] ).decode(),
                             str( message['messages'][0]['sizeEstimate'] ),
                             base64.urlsafe_b64decode( message['messages'][0]['payload']['body']['data'] ).decode()
                             ] )



    else:
        header_body.extend( [
                     
                     str( message['messages'][0]['payload']['body']['size'] ),
                     base64.urlsafe_b64decode( message['messages'][0]['payload']['body']['data'] ).decode(),
                     str( message['messages'][0]['sizeEstimate'] ),
                     base64.urlsafe_b64decode( message['messages'][0]['payload']['parts'][1]['body']['data'] ).decode()
                     ] )

    csv_list.append ( header_body )
#print( csv_list )


with open('some.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_list)


thread_id = ids[0]

#print( thread_id )

message = GetThread(service, 'me', thread_id)

#message_dict = json.loads( message )  #変数2はJSON形式の文字列

"""
print( message['messages'][0]['payload']['headers'][0]['value'] )
print( message['messages'][0]['payload']['headers'][3]['value'] )
print( message['messages'][0]['payload']['headers'][13]['value'] )
print( message['messages'][0]['payload']['headers'][17]['value'] )
print( message['messages'][0]['payload']['headers'][18]['value'] )
print( message['messages'][0]['payload']['headers'][19]['value'] )
print( message['messages'][0]['payload']['headers'][20]['value'] )
#Content-Transfer-Encoding
print( message['messages'][0]['payload']['parts'][0]['headers'][1]['value'] )

print( message['messages'][0]['payload']['parts'][0]['body']['size'] )

print( message['messages'][0]['payload']['parts'][0]['body']['data'] )
#print( base64.urlsafe_b64decode( message['messages'][0]['payload']['parts'][0]['body']['data'] ).decode() )

print( message['messages'][0]['sizeEstimate'] )
#print( base64.urlsafe_b64decode( message['messages'][0]['payload']['parts'][1]['body']['data'] ).decode() )
"""


#csv_strings = "Delivered-To,Return-Path,Date,Message-ID,Subject,From,To,Content-Transfer-Encoding,size,data,data,size"

lfcode = "¥n"

csv_strings = ""

HEADERS = ( ("Delivered-To", 0), ("Return-Path", 3), ("Message-ID", 13 ), ("Subject", 17 ), ("From", 18 ), ("To", 19 ), ("Content-Transfer-Encoding", 20 ) )

#header_list = [ "Delivered-To", "Return-Path,Date", "Message-ID,Subject", "From,To", "Content-Transfer-Encoding", "size", "data", "data", "size" ]

header_colums = [ title for title, _ in HEADERS ]
header_body = [ message['messages'][0]['payload']['headers'][val]['value'] for _, val in HEADERS ]


header_colums.extend( [ "Content-Transfer-Encoding", "size", "data", "size", "data" ] )

header_body.extend( [
                                        message['messages'][0]['payload']['parts'][0]['headers'][1]['value'],
                                        str( message['messages'][0]['payload']['parts'][0]['body']['size'] ),
                                        base64.urlsafe_b64decode( message['messages'][0]['payload']['parts'][0]['body']['data'] ).decode(),
                                        str( message['messages'][0]['sizeEstimate'] ),
                                        base64.urlsafe_b64decode( message['messages'][0]['payload']['parts'][1]['body']['data'] ).decode()
                                        ] )

print( header_body )

"""
csv_strings += ",".join( header_colums )

csv_strings += lfcode

csv_strings += ",".join( header_body )
"""
filename = datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"

f = open(filename, 'w') # 書き込みモードで開く
f.write( str( csv_strings ) ) # 引数の文字列をファイルに書き込む
f.close() # ファイルを閉じる



#例
#ids = [ result['id'] for result in results if result['id'] > x]
#powered = [ i*i for i in numbers ]






threads = results.get('threads', [])

if not threads:
    print('No threads found.')
else:
    
    #print( threads )
    print( len( threads ) )
    """
    f = open('001.json', 'w') # 書き込みモードで開く
    f.write( str( threads ) ) # 引数の文字列をファイルに書き込む
    f.close() # ファイルを閉じる
    """

    """
    print('id:', threads[0]['id'])
    thread = service.users().threads().get(userId='me', id=threads[0]['id']).execute()
    message = ''
    for part in thread['messages'][0]['payload']['parts']:
        message += base64.urlsafe_b64decode(part['body']['data']).decode()
    print(message)
"""





