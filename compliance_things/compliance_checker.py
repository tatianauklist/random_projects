import re
import yaml
from collections import Counter
from datetime import datetime

def check_exclusions(document,exclusions):
    compliance_flags = {}
    for line in document:
        for rule_items in rules["exclusions"]:
            word = rule_items["word"]
            if re.search(word,line):
                if word not in compliance_flags:
                    compliance_flags[word] = []
                compliance_flags[word].append(line)
    return compliance_flags
def value_getter(results):
    return len(results[1])
def sort_results(results,rules):
    by_category = {}
    for word, lines in results.items():
        for rule_item in rules["exclusions"]:
            if rule_item["word"] == word:
                category = rule_item["category"]
                if category not in by_category:
                    by_category[category] = 0
                by_category[category] += 1
    by_severity = {}
    for word, lines in results.items():
        for rule_item in rules["exclusions"]:
            if rule_item["word"] == word:
                severity = rule_item["severity"]
                if severity not in by_severity:
                    by_severity[severity] = 0
        by_severity[severity] += 1
    sorted_category = dict(sorted(by_category.items(),key=lambda x:x[1],reverse=True))
    return sorted_category,by_severity
start_time = datetime.now()
with open("legal_rules.yaml") as e:
    rules = yaml.safe_load(e)
    #for line in exclusion:
    #    exclusions.append(line.strip())
#print(rules)
with open("test_text2.txt") as t:
    document = t.readlines()
#print(document) 
boxing = len("Welcome to your new QA and Compliance Assistant.")
print(boxing * '-')
print("Welcome to your new QA and Compliance Assistant.")
print(boxing * '-')
start_scan = input("Press any key to start the scan or press 'x' to exit.")

if start_scan == 'x':
    print("Goodbye! Thanks for using")

else:
    results = check_exclusions(document,rules["exclusions"])
    end_time = datetime.now()
    for word, line in results.items():
        for rule_item in rules["exclusions"]:
            if rule_item["word"] == word:
                category = rule_item["category"]
                severity = rule_item["severity"]
                break
    category_breakdown, severity_breakdown = sort_results(results,rules)
    total_issues = len(results)
    print()
    total_time = end_time - start_time
    print(f"Scan completed in: {total_time}")
    print(boxing * '-')
    print(f"{total_issues} potential issues found.")
    print(boxing *'-')
    print("By Severity:")
    for severity, count in severity_breakdown.items():
        print(f"{severity}: {count}")
    print()
    print("By Category:")
    for category, count in category_breakdown.items():
        print(f"{category}: {count}")
    print(boxing * '-')
    continue_on = input("Would you like to see which words were hit the most? (y/n): ").lower()
    if continue_on == 'y':
        print("Exclusions Found")
        print(boxing * '-')
        x = 1
        for word, line in sorted(results.items(),key=value_getter,reverse=True):
            if len(line) > 0:
                print(f"{x}.'{word}': Found {len(line)} time(s) in document.")
                x += 1
            else:
                break
        print()    
        list_places = input("Would you like to see the exact places where the flags occur? (Y/N): ")
        print()
        if list_places == "Y":
            x = 1
            for word, lines in sorted(results.items(),key=value_getter,reverse=True):
              if len(line) > 0:
                   print(f"{x}.{word}:")
                   for line in lines:
                       print(f"{line.strip()}")
                   print()
                   x += 1

    print("Thanks come back soon!")
