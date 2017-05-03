import base64
import httplib2
import oauth2client
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


__author__ == 'Junya Kaneko <junya@mpsamurai.org>'


"""Problem:

Your customer is a company's support center.

The customer want you to develop a system that sorts their emails on gmail according to those urgency.

So, you decide to make a words dictionary by using their emails for further analyses.

Refactor this code so that it can download their all (or at least some) emails from gmail.
"""


SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'secrets/junya.json'
APPLICATION_NAME = 'pycamp-20170503'

store = Storage('secrets/gmail.json')
credentials = store.get()
if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    credentials = tools.run_flow(flow, store)

http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)

results = service.users().threads().list(userId='me').execute()
threads = results.get('threads', [])

if not threads:
    print('No threads found.')
else:
    print('id:', threads[0]['id'])
    thread = service.users().threads().get(userId='me', id=threads[0]['id']).execute()
    message = ''
    for part in thread['messages'][0]['payload']['parts']:
        message += base64.urlsafe_b64decode(part['body']['data']).decode()
    print(message)
