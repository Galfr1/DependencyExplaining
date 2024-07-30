import openpyxl
import subprocess
import os
from openai import OpenAI

#your openai api key
client = OpenAI(api_key="")


#path of the excel file
inputXlPath = ""

#loading the excel file
wb = openpyxl.load_workbook(inputXlPath)
sheet = wb.active

#array containing all the project paths from the excel file
path = []

#scanning the excel file for paths
i = 1
bool = True
while bool:
    tab = "A" + str(i)
    projectPath = sheet[tab].value
    i = i + 1
    if projectPath == None:
        bool = False
    else:
        path.append(projectPath)

#an array containing the outputs of the syft cli
cliOutputs = []

#running git clone and syft for each path
for p in path:
    u = "/tmp/" + p.split("/")[-1]
    os.mkdir(u)
    subprocess.run(["git", "clone", p, u])
    result = subprocess.check_output(['syft', u])
    cliOutputs.append(str(result.decode('utf-8')))
    subprocess.run(["rm", "-r", "-f", u])

#a new array containing the cleaned cli outputs of syft
cleanedList = []

#cleaning each cli output of syft and adding it to cleanedList array
for o in cliOutputs:
    split1 = o.split("\n")
    split1.pop(0)
    split1.pop(-1)

    split2 = []

    for s in split1:
        a = False
        s = s.split(" ")
        if s[0] == "":
            a = True
        s = [i for i in s if i != '']
        if a == True:
            s.insert(0, "")
        split2.append(s)

    cleanedList.append(split2)

#a new array with the no name dependenceies and the "(+1 Duplicates)" text removed
removedList = []

#removing the no name dependenceies and the "(+1 Duplicates)" text
for l in cleanedList:
    arrl = []
    for l1 in l:
        if l1 != []:
            if l1[0] != "":
                if l1[-1].endswith('duplicates)') or l1[-1].endswith('duplicate)'):
                    l1 = l1[:-2]
                arrl.append(l1)
    removedList.append(arrl)

#an array containing chatgpt's descreptions
finalList = []

#adding to each dependency array chatgpt's descreption
for r in removedList:
    arr = []
    for r1 in r:
        
        message = "Can you explain what the " + r1[-1] + " " + r1[0] + " dependency is doing?"

        stream = client.chat.completions.create(
           model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
           stream=True,
        )
        for part in stream:
               reply = part.choices[0].delta.content or ""

        r1.append(reply)
        arr.append(r1)
    finalList.append(arr)

#adding the results back to excel
ws2 = wb.create_sheet(title = 'Output')
ws2 = wb.get_sheet_by_name('Output')

h = 0
for f in finalList:
    projectName = path[h].split("/")[-1]
    h = h + 1
    b = h
    for f1 in f:
        ws2['A' + str(h)] = projectName
        n = 2
        for k in f1:
            if n==2:
                ws2['B' + str(b)] = k
            if n==3:
                ws2['C' + str(b)] = k
            if n==4:
                ws2['D' + str(b)] = k
            if n==5:
                ws2['E' + str(b)] = k
            n = n + 1
        b = b + 1

#saving the excel file
wb.save(inputXlPath)