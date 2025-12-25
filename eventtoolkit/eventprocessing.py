import json
import os
from datetime import datetime


def _processedEvents():
    if os.path.exists("processedEvents.json"):
        with open("processedEvents.json", "r") as f:
            processedList = json.load(f)
            processedEvents = set(processedList)
    else:
        processedEvents = set()

    return processedEvents


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

def buildReport(stats: dict, nextEvent: dict) -> str:
    today = datetime.today().strftime("%m-%d-%Y")
    report = ""
    statusCounts = stats["status counts"]
    typeCounts = stats["type counts"]
    maxRevenue = stats["max revenue"]
    report += f"Event Report: {today}\n"
    report += f"=======================\n"
    if nextEvent is None:
        report += f"Next Event: None\n"
    else:
        report += f"Next Event: {nextEvent['event ID']} on {nextEvent['event date']}\n"
    report += f"Max revenue: ${maxRevenue}\n"
    report += f"======================\n"
    report += f"Status Reports\n"
    for status in statusCounts:
        report += f"{status}: {statusCounts[status]}\n"
    report += f"=======================\n"
    report += f"Type Reports\n"
    for type in typeCounts:
        report += f"{type}: {typeCounts[type]}\n"
    return report
