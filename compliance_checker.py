import re
import yaml

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

with open("rules.yaml") as e:
    rules = yaml.safe_load(e)
    #for line in exclusion:
    #    exclusions.append(line.strip())
#print(rules)
with open("test_compliance.txt") as t:
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
    for word, line in results.items():
        for rule_item in rules["exclusions"]:
            if rule_item["word"] == word:
                category = rule_item["category"]
                severity = rule_item["severity"]
                break
    total_categories = len(category)
    total_issues = len(results)
    print(boxing * '-')
    print(f"{total_issues} potential issues found.")
    print(f"{total_categories} potentially broken rule categorys.")
    print(boxing * '-')
    print("Exact Issues Found - from most to least occurances")
    print(boxing * '-')
    for word, line in sorted(results.items(),key=value_getter,reverse=True):
        if len(line) > 0:
            print(f"'{word}': Found {len(line)} time(s) in document.")
    #list_places = input("Would you like to see the exact places where the flags occur? (Y/N): ")

    #if list_places == "Y":
    #    for word, line in results.items():
    #        if len(line) > 0:
    #            print(word)
    #            print(f"- {line}")

    print("Thanks come back soon!")
