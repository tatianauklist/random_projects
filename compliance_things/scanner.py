import re
import collections

# rules checker
def check_exclusions(document,exclusions):
    compliance_flags = {}
    for line in document:
        for rule_item in exclusions:
            word = rule_item["word"]
            category = rule_item["category"]
            severity = rule_item["severity"]
            if re.search(word,line):
                if word not in compliance_flags:
                    compliance_flags[word] = {
                        "category": category,
                        "severity": severity,
                        "lines": []
                    }
                compliance_flags[word]["lines"].append(line)
    return compliance_flags

# value getter
def value_getter(results):
    return len(results([1]))

# sort results
def sort_results(results,exclusions):
    by_category = {}
    for word, lines in results.items():
        for rule_item in exclusions:
            if rule_item["word"] == word:
                category = rule_item["category"]
                if category not in by_category:
                    by_category[category] = 0
                by_category[category] += 1
    by_severity = {}
    for word, lines in results.items():
        for rule_item in exclusions:
            if rule_item["word"] == word:
                severity = rule_item["severity"]
                if severity not in by_severity:
                    by_severity[severity] = 0
                by_severity[severity] += 1
    sorted_category = dict(sorted(by_category.items(),key=lambda x:x[1], reverse=True))
    return sorted_category,by_severity

# Exact word count breakdown
def word_list(results,exclusions):
    wordList = {}
    for word,data in results.items():
        category = data["category"]
        severity = data["severity"]
        lines = data["lines"]
        count = len(lines)
        if word not in wordList:
            wordList[word] = {
                        "category": category,
                        "severity": severity,
                        "count": 0
                    }
        if count > 0:
            wordList[word]["category"]= category
            wordList[word]["severity"] = severity
            wordList[word]["count"]= count
    return wordList