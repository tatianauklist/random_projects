# reading the text
import re

exclusion = []
o = open("exclusions.txt","r")
#content = o.read()
#print(content)

for line in o.readlines():
    word= line.strip()
    exclusion.append(word)
print(exclusion)    
o.close()

#names = {}
#while True:
#    name = input("Enter a character name or type 'done' to exit: ")
#    if name == 'done':
#        break
#    names[name] = []

f = open("test_compliance.txt")
text = f.readlines()

#lines = {}
#for word in exclusion:
#   lines[exclusion] = []

for line in text:
    for x in exclusion:
        if re.search(x,line):
            lines[x].append(line)
for x in lines:
    print(f"{x} is mentioned {len(lines[x])} times")

#for x in lines:
#    for word1,word2 in exclusion:
#        all_lines = " ".join(lines[x])
#        if word1 in all_lines and word2 in all_lines:
#            print(f"{x} is an excluded term")
#            for line in lines[x]:
#                if word1 in line:
#                    print(line)
#                if word2 in line:
#                    print(line)
        

f.close()