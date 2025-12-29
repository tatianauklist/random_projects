from logic import loadChecklist, saveChecklist
import logging

fileType = input("Are you checking software or event readiness?: \n")
data, filePath = loadChecklist(fileType)
project = data["projectName"]
header = f"Pre-Flight Check Results for {project}"
divider = "-" * len(header)
owner = data["owner"]["name"]
print(divider)
print(header.center(len(header)))
print(divider)
blockers = []
itemNumberMenu = {}
itemNumber = 1
for name, categoryData in data.items():
    if name not in ["projectName", "owner"]:
        totalChecks = len(categoryData)
        completedChecks = sum(categoryData.values())
        percentageCompleted = round((completedChecks/totalChecks) * 100,2)
        print(f"{name}: {percentageCompleted}%")
        for checkName in categoryData:
            checkValue = categoryData[checkName]
            if checkValue:
                checkValueAnimated = "✅"
            else:
                checkValueAnimated = "❌"
            print(f" {itemNumber} {checkName.capitalize()}: {checkValueAnimated}")
            itemNumberMenu[itemNumber] = {"check": checkName, "value": checkValue,"category": name}
            itemNumber += 1
            if not checkValue:
                blockers.append({'check': checkName, 'category': name})
print(divider)
header1 = f"Blockers"
print(header1.center(len(header)))
print(divider)
if len(blockers) <= 0:
    print("No blockers found 🥳")
else:
    for blocker in blockers:
        print(f"{blocker['check']} ({blocker['category']})")
print(divider)
updateNumbers = [int(x) for x in input("Please enter the number of the items you'd like to update seperated by a coma: \n").split(",")]
for item in updateNumbers:
    if item in itemNumberMenu:
        menuItem = itemNumberMenu[item]
        currentValue = menuItem['value']
        newValue = not menuItem['value']
        category = menuItem['category']
        checkName = menuItem['check']
        data[category][checkName] = newValue

print("Updating checklist...")
print(divider)
print(header.center(len(header)))
print(divider)
for name, categoryData in data.items():
    if name not in ["projectName", "owner"]:
        totalChecks = len(categoryData)
        completedChecks = sum(categoryData.values())
        percentageCompleted = round((completedChecks/totalChecks) * 100,2)
        print(f"{name}: {percentageCompleted}%")
        for checkName in categoryData:
            checkValue = categoryData[checkName]
            if checkValue:
                checkValueAnimated = "✅"
            else:
                checkValueAnimated = "❌"
            print(f" {itemNumber} {checkName.capitalize()}: {checkValueAnimated}")
            if not checkValue:
                blockers.append({'check': checkName, 'category': name})
print(divider)
print(header1.center(len(header)))
print(divider)
if len(blockers) <= 0:
    print("No blockers found 🥳")
else:
    for blocker in blockers:
        print(f"{blocker['check']} ({blocker['category']})")
print(divider)

saveChecklist(data, filePath)

