import csv
import time
def csvWriter(name, content):
    with open(name+'.csv', mode='a', newline = '') as csvfile:    
        spamwriter = csv.writer(csvfile, delimiter=',')
        for line in content:
            try:
                spamwriter.writerow(line)
            except Exception as e:
                print(e)
                print(line)

# removes 
def parseStr(string):
    parsed = ''
    for char in string:
        if str(char).isalpha() or str(char).isspace():
            parsed=parsed+char
    return parsed.strip()

