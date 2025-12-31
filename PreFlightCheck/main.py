from logic.logic import runInteractiveSession, getAvailableProjects, runAutomatedSession
import logging
from logic.cli import parseArgs

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
    else:
        runAutomatedSession()

if __name__ == "__main__":
    main()




