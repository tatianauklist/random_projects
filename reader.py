# reading the text
import re

#names = [r'Bob',r'Linda',r'Gail',r'Teddy',r'Mort',r'Gene',r'Louis',r'Tina']
names = {}
while True:
    name = input("Enter a character name or type 'done' to exit: ")
    if name == 'done':
        break
    names[name] = []

f = open("Test_Scene.txt")
text = f.readlines()

lines = {}
for name in names:
    lines[name] = []

for line in text:
    for x in names:
        if re.search(x,line):
            lines[x].append(line)

for name in lines:
    print(f"{name}: {len(lines[name])}\n {lines[name]}")


f.close()