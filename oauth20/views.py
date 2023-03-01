from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect

import google.oauth2.credentials
import google_auth_oauthlib.flow

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
    response= redirect(authorization_url)

    return response
