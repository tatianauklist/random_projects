import os
from flask import Flask
from logic.logic import loadChecklist, createReport, getAvailableProjects, loadIndex
from dotenv import load_dotenv
import os
from pathlib import Path

app = Flask(__name__)
@app.route('/')
def home():
    index = loadIndex()
    output = ""
    for project in index["projects"]:
        projectName = project["projectName"]
        countdown = project["count_down"]
        stats = project["stats"]
        blockers = len(project["blockers"])
        if blockers < 1:
            blockers = 0
        overdue = project["overdue"]
        output += f"{projectName} ({countdown} days until event)<br>"
        output += f"Blockers: {blockers}<br>"
        for category, categoryStats in stats.items():
            percentage = categoryStats["percentage"]
            completed = categoryStats["completed"]
            total = categoryStats["total_checks"]
            output += f"{category}: {completed} / {total} ({percentage}%)<br>"

    return output
@app.route('/leadership')
def leadership():
    index = loadIndex()
    output = ""
    for project in index["projects"]:
        projectName = project["projectName"]
        countdown = project["count_down"]
        blocker_count = len(project["blockers"])
        blockers = project["blockers"]
        overdue = project["overdue"]
        if len(overdue) < 1:
            overdue = 0
        output += f"{projectName} ({countdown} days until event)<br>"
        output += f"Blockers: {blocker_count}<br>"
        output += f"Overdue: {overdue}<br>"
        if blocker_count < 1:
            output += f"No blockers found"
        output += "Program Blockers<br>"
        for name in blockers:
            blocker_data = blockers[name]
            categoryName = blocker_data["category"]
            severity = blocker_data["severity"]
            if categoryName == "program":
                len(blockers)
                output += f"{name} - {severity}<br>"
    output += "<br>"

    return output

@app.route('/team')
def team():
    index = loadIndex()
    output = ""
    for project in index["projects"]:
        projectName = project["projectName"]
        countdown = project["count_down"]
        blocker_count = len(project["blockers"])
        blockers = project["blockers"]
        overdue = project["overdue"]
        output += f"{projectName} ({countdown} days until event)<br>"
        high_blockers = []
        medium_blockers = []
        low_blockers = []
        for name in blockers:
            blocker_data = blockers[name]
            categoryName = blocker_data["category"]
            severity = blocker_data["severity"]
            if severity == "high":
                high_blockers.append((categoryName, name))
            if severity == "medium":
                medium_blockers.append((categoryName, name))
            if severity == "low":
                low_blockers.append((categoryName, name))
        if len(overdue) < 1:
            output += f"No overdue items found<br>"
        else:
            for name in overdue:
                overdue_data = overdue[name]
                categoryName = overdue_data["category"]
                due_date = overdue_data["due_date"]
                severity = overdue_data["severity"]
                output += f"{name} - {categoryName} - {severity}<br>"
        output += " ‼️ High Blockers ‼️<br>"
        for category, name in high_blockers:
            output += f"{name}  - {category}<br>"
        output += "❗ Medium Blockers ❗<br>"
        for category, name in medium_blockers:
            output += f"{name}  - {category}<br>"
        output += "⚠️ Low Blockers ⚠️<br>"
        for category, name in low_blockers:
            output += f"{name}  - {category}<br>"
    return output








if __name__ == '__main__':
    app.run(debug=True)
