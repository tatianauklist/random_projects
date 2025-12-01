import re
import yaml
from scanner import check_exclusions, value_getter, sort_results, word_list
from collections import Counter
from datetime import datetime
from reporting import format_summary_table, build_word_table

intro = "Press any key to start the scan or press 'x' to exit"
boxing = len(intro)
border = boxing * '-'
print(border)
print("Welcome to Your New Assistant")
print(border)
menu = input("Please choose a document to read:\n1. Amazon's T&C\n2. Meta's Terms of Use\n3. Canva's Content License Agreement\n4. 23 and Me's Terms of Service\n")
if menu == '1':
    with open("amazon_toc.txt") as t:
        document = t.readlines()
    with open("amazon.yaml") as e:
        rules = yaml.safe_load(e)
elif menu == '2':
    with open("meta_community.txt") as t:
        document = t.readlines()
    with open("meta.yaml") as e:
        rules = yaml.safe_load(e)
elif menu == '3':
    with open("canva_tou.txt") as t:
        document = t.readlines()
    with open("canva.yaml") as e:
        rules = yaml.safe_load(e)
elif menu == '4':
    with open("23andme.txt") as t:
        document = t.readlines()
    with open("23andme.yaml") as e:
        rules = yaml.safe_load(e)


start_scan = input("Press any key to start the scan or press 'x' to exit\n")
start_time = datetime.now()
if start_scan == 'x':
    print("Goodbye! Thanks for using")

else:
    results = check_exclusions(document,rules["exclusions"])
    category_breakdown, severity_breakdown = sort_results(results,rules["exclusions"])
    end_time = datetime.now()
    total_time = end_time - start_time
    print(border)
    print(f"Scan completed at: {end_time}")
    print(f"Total scan time: {total_time}")
    print(border)
    wordList = word_list(results, rules["exclusions"])
    print("Summary")
    print()
    for i in format_summary_table(severity_breakdown,category_breakdown):
        print(i)
    print()
    print("Word Breakdown")
    for i in build_word_table(wordList):
        print(i)

    
    
    