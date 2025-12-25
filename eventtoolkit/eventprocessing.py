import json
import os
from datetime import datetime


def _processedEvents(data:list) -> dict:
    if os.path.exists("processedEvents.json"):
        with open("processedEvents.json", "r") as f:
            try:
                processedList = json.load(f)
                processedEvents = set(processedList)
            except json.decoder.JSONDecodeError:
                processedEvents = set()
    else:
        processedEvents = set()
    newEvents = 0
    skippedEvents = 0
    for row in data:
        eventDate, eventID, eventSize, eventType, eventStatus, eventRevenue = row
        if eventID in processedEvents:
            skippedEvents += 1
        else:
            processedEvents.add(eventID)
            newEvents += 1
    with open("processedEvents.json", "w") as f:
        processedList = list(processedEvents)
        json.dump(processedList, f)

    return {"new events": newEvents, "skipped events": skippedEvents}




def _getEventStats(data: list) -> dict:
    statusCounts = {}
    typeCounts = {}
    maxRevenue = 0

    for event in data:
        eventDate, eventID, eventSize, eventType, eventStatus, eventRevenue = event
        eventRevenueFloat = float(eventRevenue)
        if eventStatus not in statusCounts:
            statusCounts[eventStatus.strip()] = 1
        else:
            statusCounts[eventStatus] = statusCounts[eventStatus] + 1
        if eventType not in typeCounts:
            typeCounts[eventType] = 1
        else:
            typeCounts[eventType] = typeCounts[eventType] + 1
        if eventRevenueFloat > maxRevenue:
            maxRevenue = eventRevenueFloat

    return {"status counts": statusCounts, "type counts": typeCounts, "max revenue": maxRevenue}

def getNextEvent(data: list) -> dict:
    nextEvent = None
    nextEventDate = None
    for event in data:
        eventDate, eventID, eventSize, eventType, eventStatus, eventRevenue = event
        eventDate = datetime.strptime(eventDate, "%m-%d-%Y")
        today = datetime.today()
        if eventDate > today:
            if nextEvent is None or eventDate < nextEventDate:
                nextEvent = eventID
                nextEventDate = eventDate
    if nextEvent is not None:
        return {"event ID": nextEvent, "event date": nextEventDate.strftime("%m-%d-%Y")}
    else:
        return {"event ID": None, "event date": None}

def buildReport(stats: dict, nextEvent: dict, processedEvents: dict) -> str:
    today = datetime.today().strftime("%m-%d-%Y")
    report = ""
    statusCounts = stats["status counts"]
    typeCounts = stats["type counts"]
    maxRevenue = stats["max revenue"]
    newEvents = processedEvents["new events"]
    report += f"Event Report: {today}\n"
    report += f"=======================\n"
    if nextEvent is None:
        report += f"Next Event: None\n"
    else:
        report += f"Next Event: {nextEvent['event ID']} on {nextEvent['event date']}\n"
    report += f"New Events Processed: {newEvents}\n"
    report += f"Max revenue: ${maxRevenue}\n"
    report += f"======================\n"
    report += f"Status Reports\n"
    for status in statusCounts:
        report += f"{status}: {statusCounts[status]}\n"
    report += f"=======================\n"
    report += f"Type Reports\n"
    for type in typeCounts:
        report += f"{type}: {typeCounts[type]}\n"
    report += f"========================\n"
    return report

def saveReport(report: str):
    with open("report.txt", "a") as f:
        f.write(report)

