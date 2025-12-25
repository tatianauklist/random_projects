import os
from infra import getAuthenticatedService
import logging
import json
from datetime import datetime
from eventprocessing import _processedEvents, getNextEvent, _getEventStats, buildReport, saveReport

## configure logging so that the things get logged
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

SHEETS_ID = input("Enter sheet ID: ")
RANGE = "REF!A2:F"

#Checking to see if there are valid path and assigns the creds
service = getAuthenticatedService("sheets",access=["write"])
results = service.spreadsheets().values().get(spreadsheetId=SHEETS_ID,range=RANGE).execute()

data = results["values"]
if not results:
    logging.warning("No data found.")
logging.info(f"Processing new events for sheet {SHEETS_ID}...")
processedEvents = _processedEvents(data)
logging.info(f"Getting Event Stats...")
stats = _getEventStats(data)
logging.info(f"Grabbing Next Event...")
nextEvent = getNextEvent(data)
logging.info(f"Building report...")
report = buildReport(stats, nextEvent,processedEvents)
logging.info(f"DONE")
print("\n")
print(report)
save = input("Would you like to save the report for your timeline? (y/n): ")

if "y" in save.lower():
    logging.info(f"Saving report as report.txt...")
    saveReport(report)
    logging.info(f"DONE")

else:
    logging.info(f"Thanks for using. Goodbye!")

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
