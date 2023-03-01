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
REDIRECT = 'https://convin-backend-task.ayushr1.repl.co/rest/v1/calendar/redirect'


def index(request):
    button_html = '<a href="https://convin-backend-task.ayushr1.repl.co/rest/v1/calendar/init/">Login with Google</a>'
    return HttpResponse(button_html)


@api_view(['GET'])
def GoogleCalendarInitView(request):
    # Initialize the OAuth2 flow using the client secrets file and specified scopes
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CREDENTIALS_SECRET, scopes=SCOPES)

    # Set the redirect URI for the flow
    flow.redirect_uri = REDIRECT

    # Generate an authorization URL for the user to grant access to the specified scopes
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    # Store the generated state in the user's session for later verification
    request.session['state'] = state

    # Redirect the user to the generated authorization URL to complete the OAuth2 flow
    response = redirect(authorization_url)

    return response


@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    try:
        # Check if the 'state' parameter is present in the session
        state = request.session['state']

        # Create an OAuth flow object and set the redirect URI and state parameter
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CREDENTIALS_SECRET, scopes=SCOPES, state=state)
        flow.redirect_uri = REDIRECT

        # Get the authorization response from the request object
        authorization_response = request.get_full_path()

        # Exchange the authorization code for a token
        flow.fetch_token(authorization_response=authorization_response)

        # Get the credentials from the OAuth flow and save them in the session
        credentials = flow.credentials
        request.session['credentials'] = credentials_to_dict(credentials)

        # Check if the credentials are present in the session
        if 'credentials' not in request.session:
            # Redirect the user to the initial authentication view if the credentials are not present
            return redirect('v1/calendar/init')

        # Build the Google Calendar API client using the saved credentials
        credentials = google.oauth2.credentials.Credentials(
            **request.session['credentials'])
        service = googleapiclient.discovery.build(
            'calendar', 'v3', credentials=credentials, static_discovery=False)

        # Get the list of calendars for the authenticated user
        calendar_list = service.calendarList().list().execute()

        # Get the ID of the first calendar in the list
        calendar_id = calendar_list['items'][0]['id']

        # Get the list of events for the selected calendar
        events = service.events().list(calendarId=calendar_id).execute()

        # Create an empty list to store the event data
        events_list_append = []

        # Check if any events were returned
        if not events['items']:
            # Return an error message if no events were found
            print('No data found.')
            return Response({"message": "No data found or user credentials invalid."})
        else:
            # Append each event to the list
            for events_list in events['items']:
                events_list_append.append(events_list)
            # Return the list of events as a JSON response
            return Response({"events": events_list_append})

    except:
        # Handle any exceptions by redirecting the user to the initial authentication view
        button_html = '<a href="https://convin-backend-task.ayushr1.repl.co/rest/v1/calendar/init/">Error Please Login again</a>'
        return HttpResponse(button_html)


# Define a helper function to convert credentials to a dictionary

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
