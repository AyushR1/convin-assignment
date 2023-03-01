from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# solves insecure transport error
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CREDENTIALS_SECRET = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/calendar']
REDIRECT = 'http://127.0.0.1:8000/rest/v1/calendar/redirect'


def index(request):
    button_html = '<a href="http://127.0.0.1:8000/rest/v1/calendar/init/">Login with Google</a>'
    return HttpResponse(button_html)


@api_view(['GET'])
def GoogleCalendarInitView(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CREDENTIALS_SECRET, scopes=SCOPES)

    flow.redirect_uri = REDIRECT

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    request.session['state'] = state
    response = redirect(authorization_url)

    return response


@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    state = request.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CREDENTIALS_SECRET, scopes=SCOPES, state=state)
    flow.redirect_uri = REDIRECT

    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    if 'credentials' not in request.session:
        return redirect('v1/calendar/init')

    credentials = google.oauth2.credentials.Credentials(
        **request.session['credentials'])

    service = googleapiclient.discovery.build(
        'calendar', 'v3', credentials=credentials)

    calendar_list = service.calendarList().list().execute()

    calendar_id = calendar_list['items'][0]['id']

    events = service.events().list(calendarId=calendar_id).execute()

    events_list_append = []
    if not events['items']:
        print('No data found.')
        return Response({"message": "No data found or user credentials invalid."})
    else:
        for events_list in events['items']:
            events_list_append.append(events_list)
        return Response({"events": events_list_append})


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
