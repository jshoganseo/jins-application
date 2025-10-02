import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd
import json


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
service_account_info = json.loads(st.secrets["credentials"]["creds"])
CALENDAR_ID = st.secrets["credentials"]["username"]  
credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

now = datetime.utcnow().isoformat() + 'Z'
events_result = service.events().list(
    calendarId=CALENDAR_ID,
    timeMin=now,
    maxResults=50,
    singleEvents=True,
    orderBy='startTime'
).execute()

events = events_result.get('items', [])

st.title("📅 Upcoming Events")

if not events:
    st.info("No upcoming events found.")
else:
    event_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        event_list.append({
            "Event": event.get('summary', 'No Title'),
            "Start": start,
            "End": end,
            "Description": event.get('description', '')
        })

    df = pd.DataFrame(event_list)
    st.dataframe(df, use_container_width=True)

embed_url = f"https://calendar.google.com/calendar/embed?src={CALENDAR_ID}&ctz=UTC"
st.markdown("### View Calendar")
st.components.v1.iframe(embed_url, width=800, height=600)
