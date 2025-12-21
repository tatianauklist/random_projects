import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging
import json
from datetime import datetime

## configure logging so that the things get logged
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS_FILE = "credentials.json"
SHEETS_ID = "1mpB5Vead4C9s2wQBBlhQOeGqrMtATcK_9QsLUhHYhFM"
creds = None
RANGE = "REF!A2:F"

#Checking to see if there are valid path and assigns the creds
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json",SCOPES)

# Checking if there are valid creds available
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)

# save creds for next run
    with open("token.json","w") as token:
        token.write(creds.to_json())

# checking for processed events
if os.path.exists("processedEvents.json"):
    with open("processedEvents.json","r") as f:
        processedList = json.load(f)
        processedEvents = set(processedList)
else:
    processedEvents = set()

try:
    logging.info("Connecting to Google Sheets API...")
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    results = (sheet.values().get(spreadsheetId=SHEETS_ID, range=RANGE).execute())
    values = results.get("values",[])

    if not values:
        logging.warning("No data found.")
    statusCounts = {}
    typeCounts = {}
    newEvents = 0
    skippedEvents = 0
    nextEvent = None
    nextEventDate = None
    for row in values:
        eventDate, eventID, eventSize, eventType, eventStatus, eventRevenue = row
        if eventID in processedEvents:
            skippedEvents += 1
            continue
        else:
            processedEvents.add(eventID)
            newEvents += 1
        eventDate = datetime.strptime(eventDate, "%m-%d-%Y")
        today = datetime.now()
        if eventDate > today:
            if nextEvent is None or eventDate < nextEventDate:
                nextEvent = eventID
                nextEventDate = eventDate
        if eventStatus not in statusCounts:
            statusCounts[eventStatus.strip()] = 1
        else:
            statusCounts[eventStatus] += 1
        if eventType not in typeCounts:
            typeCounts[eventType] = 1
        else:
            typeCounts[eventType] += 1
        logging.debug(f"Processing event: {eventID}, status: {eventStatus}, revenue: {eventRevenue}")


    logging.info(f"Done!, {len(values)} events processed.")
    logging.info(f"Status Counts: {statusCounts}")
    logging.info(f"Type Counts: {typeCounts}")
    logging.info(f"New Events: {newEvents}")
    logging.info(f"Skipped Events: {skippedEvents}")
    if nextEvent is not None:
        logging.info(f"Next Event: {nextEvent} on {nextEventDate.strftime('%m-%d-%Y')}")
    else:
        logging.info("No upcoming events found")

    logging.info(f"Writing results to file...")
    with open("processedEvents.json","w") as f:
        json.dump(list(processedEvents),f)
    logging.info(f"{newEvents} events processed and added to processedEvents.json.")


except HttpError as err:
    logging.error(f"Failed to connect to Google Sheets API: {err}")