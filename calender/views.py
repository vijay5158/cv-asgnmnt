from django.shortcuts import redirect

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from rest_framework.decorators import api_view
from rest_framework.response import Response
from convinass.settings import SCOPES,REDIRECT_URL,API_SERVICE_NAME,API_VERSION,CLIENT_SECRETS_FILE

import os


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'



@api_view(['GET'])
def GoogleCalendarInitView(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    print(flow)
    flow.redirect_uri = REDIRECT_URL

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    request.session['state'] = state

    return Response({"authorization_url": authorization_url})


@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    state = request.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = REDIRECT_URL

    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)


    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    if 'credentials' not in request.session:
        return redirect('v1/calendar/init')

    credentials = google.oauth2.credentials.Credentials(
        **request.session['credentials'])

    service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    calendar_list = service.calendarList().list().execute()

    calendar_id = calendar_list['items'][0]['id']

    events  = service.events().list(calendarId=calendar_id).execute()

    events_list_append = []
    if not events['items']:
        print('No data found.')
        return Response({"message": "No data found or user credentials invalid."})
    else:
        for events_list in events['items']:
            events_list_append.append(events_list)
            return Response({"events": events_list_append})
    return Response({"error": "calendar event aren't here"})


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}