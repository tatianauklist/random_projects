import os
from infra import getAuthenticatedService
import logging
import json
from datetime import datetime

## configure logging so that the things get logged
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

SHEETS_ID = input("Enter sheet ID: ")
RANGE = "REF!A2:F"

#Checking to see if there are valid path and assigns the creds
service = getAuthenticatedService("sheets",access=["write"])
results = service.spreadsheets().values().get(spreadsheetId=SHEETS_ID,range=RANGE).execute()

# checking for processed events
if os.path.exists("processedEvents.json"):
    with open("processedEvents.json","r") as f:
        processedList = json.load(f)
        processedEvents = set(processedList)
else:
    processedEvents = set()


if not results:
    logging.warning("No data found.")
statusCounts = {}
typeCounts = {}
newEvents = 0
skippedEvents = 0
nextEvent = None
nextEventDate = None
for row in results["values"]:
    eventDate, eventID, eventSize,eventType, eventStatus, eventRevenue = row
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


logging.info(f"Done!, {len(results)} events processed.")
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
