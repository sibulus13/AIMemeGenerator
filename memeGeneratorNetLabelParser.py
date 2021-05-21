import requests
import os
import string
# import nltk #natural language tool kit
from bs4 import BeautifulSoup
# import urllib.request as urllib2
from urllib.request import Request, urlopen
import urllib.error
import re
from utility import *

folder = r"Z:\sibroot\repo\personal\AIMemeGenerator"
os.chdir(folder)

url = 'https://memegenerator.net/Willy-Wonka/images/popular/alltime/page/1'
# manual split
base = 'https://memegenerator.net/'
memeTitle = 'Willy-Wonka'
end = "/images/popular/alltime/page/" #append pg# at end


def parse_labels(title, first_pg_num, last_pg_num):
    lines = []
    link = base+title+end
    csvfile = open(title+'memegenerator.csv', mode = 'a', newline = '')
    spamwriter = csv.writer(csvfile, delimiter = ',')
    for i in range(first_pg_num, last_pg_num):
        try:
            url = link+str(i)
            print('pg#', i, url)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html_page = urlopen(req).read()
            soup = BeautifulSoup(html_page, features="html.parser")
            str0 = soup('div', {"class":"optimized-instance-text0"})
            str1 = soup('div', {"class":"optimized-instance-text1"})
            for j in range(0, len(str0),2): #skip duplicates
                line0 = str0[j].text.lower()
                line1 = str1[j].text.lower()
                if len(line0) > 0:
                    if line0[-1] != '?':
                        line0 += '?'
                if len(line1) > 0:
                    if line1[-1] != '.':
                        line1 += '.'
                line = [line0+'/n'+line1, line0, line1, url, i]
                try:
                    spamwriter.writerow(line)
                except UnicodeEncodeError as e:
                    print(e)
                    print('skipping', line)
                    # pass
        except Exception as e:
            print(e)
            print('you fucked up')
            break

    csvfile.close()
    return lines
                
start = time.time()   
print('parsing')
lines = parse_labels(memeTitle, 7821, 10000)
# print('printing', time.time()-start, len(lines))
# csvWriter(memeTitle+"memegenerator", lines)
print('done', time.time()-start)

# takes about 5hrs to load (1,5000)