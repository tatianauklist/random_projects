import yaml

def loadChecklist(fileType):
    if "software" in fileType:
        filePath = '/Users/tatianauklist/plotholes/PreFlightCheck/configs/softwaresample.yaml'
        with open(filePath, 'r') as f:
            data = yaml.safe_load(f)
    elif "event" in fileType:
        filePath = '/Users/tatianauklist/plotholes/PreFlightCheck/configs/eventssample.yaml'
        with open(filePath, 'r') as f:
            data = yaml.safe_load(f)
    return data, filePath

def saveChecklist(data, filePath):
    with open(filePath, 'w') as f:
        yaml.dump(data,f, sort_keys=False)

def generateReport(data):
    project = data["projectName"]
    header = f"Pre-Flight Check Results for {project}"
    divider = "-" * len(header)
    owner = data["owner"]["name"]
    yield divider
    yield header.center(len(header))
    yield divider
    blockers = []
    itemNumberMenu = {}
    itemNumber = 1
    for name, categoryData in data.items():
        if name not in ["projectName", "owner"]:
            totalChecks = len(categoryData)
            completedChecks = sum(categoryData.values())
            percentageCompleted = round((completedChecks / totalChecks) * 100, 2)
            yield f"{name}: {percentageCompleted}%"
            for checkName in categoryData:
                checkValue = categoryData[checkName]
                if checkValue:
                    checkValueAnimated = "✅"
                else:
                    checkValueAnimated = "❌"
                yield(f" {itemNumber} {checkName.capitalize()}: {checkValueAnimated}")
                itemNumberMenu[itemNumber] = {"check": checkName, "value": checkValue, "category": name}
                itemNumber += 1
                if not checkValue:
                    blockers.append({'check': checkName, 'category': name})
    yield divider
    header1 = f"Blockers"
    yield header1.center(len(header))
    yield divider
    if len(blockers) <= 0:
        yield "No blockers found 🥳"
    else:
        for blocker in blockers:
            yield f"{blocker['check']} ({blocker['category']})"
    yield divider

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






