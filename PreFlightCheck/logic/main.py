from logic import loadChecklist, saveChecklist, generateReport, getNumberedChecks, updateChecklist
import logging

fileType = input("Are you checking software or event readiness?: \n")
data, filePath = loadChecklist(fileType)
report = generateReport(data)
for i in report:
    print(i)
numberedCheck = getNumberedChecks(data)
updateDecision = input("Would you like to update anything in the checklist? (y/n)\n").lower()
if updateDecision == "y":
    updateNumbers = [int(x) for x in input("Please enter the number of the items you'd like to update seperated by a coma: \n").split(",")]
    updatedData = updateChecklist(data, numberedCheck, updateNumbers)
    print("Updating checklist...")
    reportUpdated = generateReport(updatedData)
    for i in reportUpdated:
        print(i)
    print("Saving checklist...")
    saveChecklist(updatedData,filePath)
else:
    print("No changes made to file. Goodbye!")

