import yaml
import glob
import os
from datetime import datetime, timedelta
import json
from google.cloud import storage
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def getAvailableProjects():
    client = storage.Client()
    bucket = client.get_bucket("pre-flight-checklists")
    blobs = bucket.list_blobs()
    projects = [blob.name.replace(".yaml","") for blob in blobs if blob.name.endswith(".yaml")]
    return projects

def loadChecklist(projectName):
    client = storage.Client()
    bucket = client.get_bucket("pre-flight-checklists")
    blob = bucket.blob(f"{projectName}.yaml")
    yaml_content = blob.download_as_string()
    data = yaml.safe_load(yaml_content)
    return data, f"{projectName}.yaml"

def loadIndex():
    client = storage.Client()
    bucket = client.get_bucket("weekly-event-reports")
    blob = bucket.blob("reports/index.json")
    json_contents = blob.download_as_string()
    data = json.loads(json_contents)
    return data

def runInteractiveSession(projectName):
    data, filePath = loadChecklist(projectName)
    report, blockers, overdue = createReport(data)
    humanReport = renderHumanReport(report,blockers, overdue)
    for i in humanReport:
        print(i)
    numberedCheck = getNumberedChecks(data)
    updateDecision = input("Would you like to update anything in the checklist? (y/n)\n").lower()
    if updateDecision == "y":
        updateNumbers = [int(x) for x in input(
            "Please enter the number of the items you'd like to update separated by a coma: \n").split(",")]
        updatedData = updateChecklist(data, numberedCheck, updateNumbers)
        print("Updating checklist...")
        updatedReport, updatedBlockers, updatedOverdue = createReport(updatedData)
        reportUpdated = renderHumanReport(updatedReport,updatedBlockers,updatedOverdue)
        for i in reportUpdated:
            print(i)
        print("Saving checklist...")
        saveChecklist(updatedData, filePath)
    else:
        print("No changes made to file. Goodbye!")

def runAutomatedSession():
    logger.info("Starting weekly automated session...")
    index = {"projects":[]}
    date = datetime.today().strftime("%m-%d-%Y")
    projects = getAvailableProjects()
    logger.info(f"Found {len(projects)} projects")
    os.makedirs("reports/",exist_ok=True)
    for project in projects:
        logger.info(f"Processing project: {project}")
        try:
            data, filePath = loadChecklist(project)
            report, blockers, overdue = createReport(data)
            projectName = report["projectName"]
            countDown = report["count_down"]
            projectEntry = {"projectName": projectName,"count_down": countDown,"blockers": blockers, "overdue": overdue, "stats": {}}
            for name, categoryData in report.items():
                if name not in ["projectName", "count_down"]:
                    total_checks = len(categoryData.keys())
                    completed_checks = 0
                    for checkName in categoryData:
                        check_data = categoryData[checkName]
                        if check_data["completed"]:
                            completed_checks += 1
                        else:
                            continue
                    percentage = completed_checks / total_checks * 100
                    projectEntry["stats"][name] = {"completed": completed_checks, "percentage": percentage,"total_checks": total_checks}
            index["projects"].append(projectEntry)

            saveToGCS_JSON(report,f'{projectName}-{date}.json')
            logger.info(f"Successfully saved report for {projectName}")
        except Exception as e:
            logging.error(f"Failed to process {project}: {str(e)}")
            continue
    saveToGCS_JSON(index,"index.json")
    logger.info(f"Automated session complete")

def saveChecklist(data, filePath):
    with open(filePath, 'w') as f:
        yaml.dump(data,f, sort_keys=False)

    filename = os.path.basename(filePath)
    saveToGCS_YAML(data,filename)

def getNumberedChecks(data):
    itemNumberMenu = {}
    itemNumber = 1
    event_date_str = data["event_date"]
    event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
    for name, categoryData in data.items():
        if name not in ["projectName", "owner","event_date"]:
            for checkName in categoryData:
                check_data = categoryData[checkName]
                completed = check_data["completed"]
                offset_date = check_data["due_date"]
                offset_int = int(offset_date)
                due_date = (event_date - timedelta(days=offset_int)).strftime("%Y-%m-%d")
                itemNumberMenu[itemNumber] = {"check": checkName,"completed": completed, "category": name, "due_date": due_date}
                itemNumber += 1
    return itemNumberMenu

def updateChecklist(data,numberedChecks,updateNumbers):
    project = data["projectName"]
    for item in updateNumbers:
        if item in numberedChecks:
            menuItem = numberedChecks[item]
            currentValue = menuItem["completed"]
            newValue = not menuItem["completed"]
            category = menuItem["category"]
            checkName = menuItem["check"]
            data[category][checkName]["completed"] = newValue

    return data

def createReport(data):
    report = {}
    today = datetime.today()
    project = data["projectName"]
    event_date_str = data["event_date"]
    event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
    countdown = (event_date.date() - today.date()).days
    blockers = {}
    overdue = {}

    report["projectName"] = project
    report["count_down"] = countdown
    for name, categoryData in data.items():
        if name not in ["projectName", "owner","event_date"]:
            report[name] = {}
            for checkName in categoryData:
                report[name][checkName] = {}
                check_data = categoryData[checkName]
                offset_date = check_data["due_date"]
                offset_int = int(offset_date)
                due_date = (event_date - timedelta(days=offset_int)).strftime("%Y-%m-%d")
                severity = check_data["severity"]
                completed = check_data["completed"]
                if not completed:
                    blockers[checkName] = {"category": name, "due_date": due_date, "severity": severity}
                if due_date < datetime.today().strftime("%Y-%m-%d") and not completed:
                    overdue[checkName] = {"category": name, "due_date": due_date, "severity": severity}
                report[name][checkName] = {"due_date": due_date,"severity": severity,"completed": completed}


    return report, blockers, overdue

def renderHumanReport(report,blockers,overdue):
    project = report["projectName"]
    count_down = report["count_down"]
    header = f"Pre-Flight Check Results for {project}"
    divider = "-" * len(header)
    today = datetime.today().strftime("%Y-%m-%d")
    yield divider
    yield header.center(len(header))
    yield divider
    yield f"{count_down} days until event"
    yield divider
    yield "Blockers"
    if len(blockers) > 0:
        for checkName in blockers:
            check_data = blockers[checkName]
            due_date = check_data["due_date"]
            severity = check_data["severity"]
            category = check_data["category"]
            yield f"{checkName} ({category}) - {severity}: {due_date} "
    else:
        yield "No blockers found"
    yield divider
    yield f"Overdue Items"
    if len(overdue) > 0:
        for checkName in overdue:
            check_data = overdue[checkName]
            due_date = check_data["due_date"]
            overdue_by = (due_date - today).days
            category = check_data["category"]
            severity = check_data["severity"]
            yield f"{checkName} ({category}) - {severity}: {overdue_by} "
    else:
        yield "No overdue items found"
    yield divider
    itemNumberMenu = {}
    itemNumber = 1
    for name, categoryData in report.items():
        if name not in ["projectName", "count_down"]:
            yield name.capitalize()
            for checkName in categoryData:
                check_data = categoryData[checkName]
                due_date = check_data["due_date"]
                severity = check_data["severity"]
                completed = check_data["completed"]
                if not completed:
                    completed_visual = "❌"
                else:
                    completed_visual = "✅"
                yield f"{itemNumber}){checkName} - {severity}: {completed_visual}\ndue: {due_date} "
                itemNumberMenu[itemNumber] = {"checkName": checkName, "completed": completed, "category": name, "due_date": due_date}
                itemNumber += 1






    yield divider


def saveToGCS_JSON(report,filename):
    client = storage.Client()
    bucket = client.get_bucket("weekly-event-reports")
    blob = bucket.blob(f'reports/{filename}')
    blob.upload_from_string(json.dumps(report, indent=2))

def saveToGCS_YAML(data,filename):
    client = storage.Client()
    bucket = client.get_bucket("pre-flight-checklists")
    blob = bucket.blob(filename)
    blob.upload_from_string(yaml.dump(data, sort_keys=False))

def createChecklist(templateType, projectName, owner, event_date):
    with open(f"configs/{templateType}.yaml","r") as f:
        template = yaml.safe_load(f)

    events = {"projectName": projectName, "owner": owner, "event_date": event_date}
    for category in template["categories"]:
        events[category] = {}
        for checks in template["categories"][category]:
            checks_data = template["categories"][category][checks]
            completed = False
            severity = checks_data["severity"]
            due_date_offset = checks_data["due_date_offset"]
            event_check = {"due_date": due_date_offset, "completed": completed, "severity": severity}
            events[category][checks] = event_check
    saveToGCS_YAML(events,f"{projectName}.yaml")
    return "Checklist successfully created"















