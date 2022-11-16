from __future__ import print_function
# used google quickstart for api calls
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    creds = None
# makes this token file for auth purposes after authenticating through google which is neat
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for next time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # call the API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting upcoming events...')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=100, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # prints the start and name of the next 100 events (google forces you to set a limit, so i set a realistic testing number for now)
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            # checks to make sure that event has a name, if not, will print that there is none
            if 'summary' in event:
                print(start, event['summary'])
               
            else:
                print(start, '(No title)')

    except HttpError as error:
        print('An error occurred: %s' % error)

main()
