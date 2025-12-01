from scanner import word_list, check_exclusions, sort_results
from reporting import format_summary_table, build_word_table
import yaml

with open("meta_community.txt") as t:
        document = t.readlines()
with open("meta.yaml") as e:
        rules = yaml.safe_load(e)

results = check_exclusions(document,rules["exclusions"])
category_breakdown, severity_breakdown = sort_results(results,rules["exclusions"])
#print(results)
wordList = word_list(results,rules["exclusions"])
#print(wordList)




#print(build_word_table(wordList))
for i in build_word_table(wordList):
        print(i)


#for i in format_summary_table(severity_breakdown,category_breakdown):
#        print(i)

