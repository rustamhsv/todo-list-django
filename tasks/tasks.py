from __future__ import print_function

import json

import requests
from celery import shared_task


import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# import tasks
from tasks.models import Task
from todo_list.settings import BASE_DIR

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


# @shared_task(name='add')
# def add(x, y):
#     return x + y


@shared_task
def get_google_calendar_events(user):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    events = []
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('google-credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)

    if events:
        for event in events:
            end_date = event['end']['dateTime'][:10]
            calendar_task = Task.objects.create(
                task_name=event['summary'],
                due_date=end_date
            )
            calendar_task.user.add(user)

            calendar_task.save()

    return events


# def refresh_google_api_token(client_id, client_secret, refresh_token):
#     params = {
#         'grant_type': 'refresh_token',
#         'client_id': client_id,
#         'client_secret': client_secret,
#         'refresh_token': refresh_token,
#     }
#
#     authorization_url = "https://oauth2.googleapis.com/token"
#     response = requests.post(authorization_url, data=params)
#
#     if response.ok:
#         return response.json()
#     else:
#         return None
