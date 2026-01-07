import os
from datetime import date

from flask import Flask, render_template
from logic.logic import loadChecklist, createReport, getAvailableProjects, loadIndex
from dotenv import load_dotenv
import os
from pathlib import Path

app = Flask(__name__)

@app.route('/leadership')
def leadership():
    index = loadIndex()
    for project in index["projects"]:
        projectName = project["projectName"]
        countdown = project["count_down"]
        blockers = project["blockers"]
        overdue = project["overdue"]
        program_blockers = {}
        for name in blockers:
            blocker_data = blockers[name]
            categoryName = blocker_data["category"]
            severity = blocker_data["severity"]
            if categoryName == "program":
                program_blockers[name] = {"name": name, "severity": severity}
        project["program_blockers"] = program_blockers
        if len(overdue) > 0:
            overdue_over = {}
            for name in overdue:
                overdue_data = overdue[name]
                categoryName = overdue_data["category"]
                dueDate = overdue_data["due_date"]
                severity = overdue_data["severity"]
                overdue_over[name] = {"category": categoryName, "due_date": dueDate, "severity": severity}
            project["overdue_over"] = overdue_over
        else:
            project["overdue_over"] = None








    return render_template("leaders.html",title="Leadership Updates",posts=index)

@app.route('/team')
def team():
    index = loadIndex()
    user = {"username": "Tatiana"}
    for project in index["projects"]:
        projectName = project["projectName"]
        countdown = project["count_down"]
        blocker_count = len(project["blockers"])
        blockers = project["blockers"]
        overdue = project["overdue"]
        high_blockers = {}
        medium_blockers = {}
        low_blockers = {}
        for name in blockers:
            blocker_data = blockers[name]
            categoryName = blocker_data["category"]
            severity = blocker_data["severity"]
            if severity == "high":
                high_blockers[name] = {"category":categoryName}
            if severity == "medium":
                medium_blockers[name] = {"category":categoryName}
            if severity == "low":
                low_blockers[name] = {"category":categoryName}
        project["high_blockers"] = high_blockers
        project["medium_blockers"] = medium_blockers
        project["low_blockers"] = low_blockers
        high_overdue = {}
        medium_overdue = {}
        low_overdue = {}
        if len(overdue) < 1:
            high_overdue = 0
            medium_overdue = 0
            low_overdue = 0
        else:
            for name in overdue:
                overdue_data = overdue[name]
                categoryName = overdue_data["category"]
                due_date = overdue_data["due_date"]
                severity = overdue_data["severity"]
                if severity == "high":
                    high_overdue[name] = {"category": categoryName, "due_date": due_date}
                if severity == "medium":
                    medium_overdue[name] = {"category": categoryName, "due_date": due_date}
                if severity == "low":
                    low_overdue[name] = {"category": categoryName, "due_date": due_date}
        project["high_overdue"] = high_overdue
        project["medium_overdue"] = medium_overdue
        project["low_overdue"] = low_overdue
    return render_template("stakeholders.html",title="Team View",user=user,posts=index)


@app.route('/index')
@app.route('/')
def home():
    user = {'username': 'Tatiana'}
    posts = loadIndex()
    return render_template("index.html",title='Home',user=user,posts=posts)




if __name__ == '__main__':
    app.run(debug=True)
