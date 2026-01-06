from logic.logic import runInteractiveSession, getAvailableProjects, runAutomatedSession, createChecklist,createReport, loadChecklist, getNumberedChecks, renderHumanReport, loadIndex
from logic.cli import parseArgs
import yaml

def main():
    args = parseArgs()
    if args.project:
        runInteractiveSession(args.project)
    elif args.interactive:
        availableProjects = getAvailableProjects()
        for i in availableProjects:
            print(i)
        project = input("Which project would you like to check? ").lower().strip()
        runInteractiveSession(project)
    elif args.create:
        projectName = input("What is the name of the project you'd like to create? ").lower()
        event_date = input("What is the date of the event? (YYYY-mm-dd format) ").lower()
        owner = input("What is the owner of the project? ").lower()
        createChecklist(projectName, owner, event_date)
        runInteractiveSession(projectName)

    else:
        runAutomatedSession()

if __name__ == "__main__":
    index = loadIndex()
    print(index.keys())
    print(type(index.keys()))
    print("What's IN index['projects']:", index["projects"])





