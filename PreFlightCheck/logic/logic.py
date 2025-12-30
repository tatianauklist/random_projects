import yaml
import glob
import os

def getAvailableProjects(configDir="configs/"):
    yamlFiles = glob.glob(f"{configDir}*.yaml")
    projects = [os.path.basename(f).replace(".yaml", "") for f in yamlFiles]
    return projects

def loadChecklist(projectName, configDir = "configs/"):
    filePath = f"{configDir}{projectName}.yaml"
    with open(filePath, 'r') as f:
            data = yaml.safe_load(f)
    return data, filePath

def runInteractiveSession(projectName):
    data, filePath = loadChecklist(projectName)
    report = createReport(data)
    humanReport = renderHumanReport(report)
    for i in humanReport:
        print(i)
    numberedCheck = getNumberedChecks(data)
    updateDecision = input("Would you like to update anything in the checklist? (y/n)\n").lower()
    if updateDecision == "y":
        updateNumbers = [int(x) for x in input(
            "Please enter the number of the items you'd like to update seperated by a coma: \n").split(",")]
        updatedData = updateChecklist(data, numberedCheck, updateNumbers)
        print("Updating checklist...")
        reportUpdated = renderHumanReport(updatedData)
        for i in reportUpdated:
            print(i)
        print("Saving checklist...")
        saveChecklist(updatedData, filePath)
    else:
        print("No changes made to file. Goodbye!")


def saveChecklist(data, filePath):
    with open(filePath, 'w') as f:
        yaml.dump(data,f, sort_keys=False)

def getBlockers(data):
    blockers = []
    for name, categoryData in data.items():
        if name not in ["projectName", "owner"]:
            for checkName in categoryData:
                checkValue = categoryData[checkName]
                if not checkValue:
                    blockers.append({'check': checkName, 'category': name})
    return blockers

def getNumberedChecks(data):
    itemNumberMenu = {}
    itemNumber = 1
    for name, categoryData in data.items():
        if name not in ["projectName", "owner"]:
            for checkName in categoryData:
                checkValue = categoryData[checkName]
                itemNumberMenu[itemNumber] = {"check": checkName,"checkValue": checkValue, "category": name}
                itemNumber += 1
    return itemNumberMenu

def updateChecklist(data,numberedChecks,updateNumbers):
    project = data["projectName"]
    for item in updateNumbers:
        if item in numberedChecks:
            menuItem = numberedChecks[item]
            currentValue = menuItem["checkValue"]
            newValue = not menuItem["checkValue"]
            category = menuItem["category"]
            checkName = menuItem["check"]
            data[category][checkName] = newValue

    return data

def createReport(data):
    report = {}
    project = data["projectName"]
    report["projectName"] = project
    for name, categoryData in data.items():
        if name not in ["projectName", "owner"]:
            report[name] = {}
            report[name]["totalChecks"] = len(categoryData)
            report[name]["completedChecks"] = sum(categoryData.values())
            report[name]["percentageCompleted"] = round((report[name]["completedChecks"] / report[name]["totalChecks"]) * 100, 2)
            report[name]["checks"] = []
            for checkName in categoryData:
                report[name]["checks"].append({"check": checkName, "value": categoryData[checkName]})
    report["blockers"] = getBlockers(data)
    return report



def renderHumanReport(report):
    project = report["projectName"]
    header = f"Pre-Flight Check Results for {project}"
    divider = "-" * len(header)
    yield divider
    yield header.center(len(header))
    yield divider
    itemNumberMenu = {}
    itemNumber = 1
    for name, categoryData in report.items():
        if name not in ["projectName", "blockers"]:
            totalChecks = categoryData["totalChecks"]
            completedChecks = categoryData["completedChecks"]
            percentageCompleted = categoryData["percentageCompleted"]
            yield f"{name}: {percentageCompleted}%"
            for check in categoryData:
                checkValue = categoryData[check]
                if checkValue:
                    checkValueAnimated = "✅"
                else:
                    checkValueAnimated = "❌"
                yield f" {itemNumber} {check.capitalize()}: {checkValueAnimated}"
                itemNumberMenu[itemNumber] = {"check": check, "value": checkValue, "category": name}
                itemNumber += 1
    yield divider
    header1 = f"Blockers"
    yield header1.center(len(header))
    yield divider
    if len(report["blockers"]) <= 0:
        yield "No blockers found 🥳"
    else:
        for blocker in report["blockers"]:
            yield f"{blocker['check']} ({blocker['category']})"
    yield divider











