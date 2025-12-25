import os
from infra import getAuthenticatedService
import logging
import json
from datetime import datetime
from eventprocessing import _processedEvents, getNextEvent, _getEventStats, buildReport

## configure logging so that the things get logged
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

SHEETS_ID = input("Enter sheet ID: ")
RANGE = "REF!A2:F"

#Checking to see if there are valid path and assigns the creds
service = getAuthenticatedService("sheets",access=["write"])
results = service.spreadsheets().values().get(spreadsheetId=SHEETS_ID,range=RANGE).execute()

data = results["values"]
# checking for processed events
processedEvents = _processedEvents()


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
logging.info(f"Getting Event Stats...")
stats = _getEventStats(data)
logging.info(f"Grabbing Next Event...")
nextEvent = getNextEvent(data)
logging.info(f"Building report...")
report = buildReport(stats, nextEvent)
logging.info(f"DONE")
print(report)

#logging.info(f"Done!, {len(results)} events processed.")
#logging.info(f"Status Counts: {statusCounts}")
#logging.info(f"Type Counts: {typeCounts}")
#logging.info(f"New Events: {newEvents}")
#logging.info(f"Skipped Events: {skippedEvents}")
#if nextEvent is not None:
#    logging.info(f"Next Event: {nextEvent} on {nextEventDate.strftime('%m-%d-%Y')}")
#else:
#    logging.info("No upcoming events found")

#logging.info(f"Writing results to file...")
#with open("processedEvents.json","w") as f:
#    json.dump(list(processedEvents),f)
#logging.info(f"{newEvents} events processed and added to processedEvents.json.")
