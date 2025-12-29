from logic import loadChecklist

fileType = input("Are you checking software or event readiness?: \n")
data = loadChecklist(fileType)
project = data["projectName"]
header = f"Pre-Flight Check Results for {project}"
divider = "-" * len(header)
owner = data["owner"]["name"]
print(divider)
print(header.center(len(header)))
print(divider)
blockers = []
for name, categoryData in data.items():
    if name not in ["projectName", "owner"]:
        totalChecks = len(categoryData)
        completedChecks = sum(categoryData.values())
        percentageCompleted = round((completedChecks/totalChecks) * 100,2)
        print(f"{name}: {percentageCompleted}%")
        for checkName in categoryData:
            checkValue = categoryData[checkName]
            if checkValue:
                checkValue = "✅"
            else:
                checkValue = "❌"
            print(f"- {checkName.capitalize()}: {checkValue}")
            if checkValue not in "✅":
                blockers.append({'check': checkName, 'category': name})
print(divider)
header1 = f"Blockers"
print(header1.center(len(header)))
print(divider)
if len(blockers) <= 0:
    print("No blockers found 🥳")
else:
    for blocker in blockers:
        print(f"- {blocker['check']} ({blocker['category']})")
print(divider)







