
from __future__ import print_function
import httplib2
import os
import sys

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from datetime import *
from slackbot_settings import *

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


service = None

def initialize_service():
    global service
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_path = os.path.join(os.path.dirname(sys.argv[0]),
                                   'credentials.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def list_range(min, max):
    min = min.isoformat() + 'Z' # 'Z' indicates UTC time
    max = max.isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary', timeMin=min, timeMax=max, maxResults=1000, singleEvents=True,
        orderBy='startTime').execute()
    return events_result.get('items', [])

def add_event(event):
    service.events().insert(calendarId='primary', body=event).execute()

def delete_event(event_id):
    service.events().delete(calendarId='primary', eventId=event_id).execute()
