import re
import yaml

compliance_flags = {}
def check_exclusions(document,exclusion):
    for word in exclusions:
        compliance_flags[word] = []
    for line in document:
        for word in exclusions:
            if re.search(word,line):
                compliance_flags[word].append(line)
    return compliance_flags
def value_getter(results):
    return len(results[1])
exclusions = []
with open("exclusions.yaml") as e:
    exclusion = yaml.safe_load(e)
    #for line in exclusion:
    #    exclusions.append(line.strip())
print(exclusion)
with open("test_compliance.txt") as t:
    document = t.readlines()
#print(document)    

results = check_exclusions(document,exclusions)
for word, line in sorted(results.items(),key=value_getter,reverse=True):
    if len(line) > 0:
        print(f"'{word}': Found {len(line)} times in document.")
list_places = input("Would you like to see the exact places where the flags occur? (Y/N): ")

if list_places == "Y":
    for word, line in results.items():
        if len(line) > 0:
            print(word)
            print(f"- {line}")