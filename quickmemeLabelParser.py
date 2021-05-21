import requests
import os
import string
# import nltk #natural language tool kit
from bs4 import BeautifulSoup
# import urllib.request as urllib2
from urllib.request import Request, urlopen
import urllib.error
import re
import csv
import time
from utility import *

url = "http://www.quickmeme.com/Condescending-Wonka/page/2500"
folder = r"Z:\sibroot\repo\personal\AIMemeGenerator"
base = "http://www.quickmeme.com/"
os.chdir(folder)

def parse_labels(title,last_pg_num):
    lines = []
    link = base+title+"/page/"
    # print(link)
    for i in range(1, last_pg_num):
        try:
            url = link+str(i)
            print('pg#', i, url)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html_page = urlopen(req).read()
            soup = BeautifulSoup(html_page, features="html.parser")
            images = soup.findAll('img')

            # pgs continue without memes, but have 1 img on site
            if len(images) == 1:
                return lines    
            for image in soup.findAll('img'):
                alt = image.get('alt')
                # print(alt)
                if alt is not None:
                    alt = alt.replace('Condescending Wonka','')
                    label = alt.lower()
                    line1 = ''
                    line2 = ''
                    if '?' in label:
                        line1, line2 = label.split('?',1)
                        
                    lines.append([label, line1, line2])
                else:
                    break
        except Exception as e:
            print(e)
            print('you fucked up')
            break
    return lines
start = time.time()   
title = "Condescending-Wonka"
lines = parse_labels(title, 10000)
print('printing', time.time()-start, len(lines))
csvWriter(title+'quickmeme', lines)
print('done', time.time()-start)