# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import csv
import nltk
import os
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams

# %%
memefile = 'Willy-Wonkamemegenerator.csv' # only 500 unique words fk
labels = []
with open(memefile) as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        labels.append(row)
labels.pop(0)


# %%
def list2probdict(alist):
    probdict={k:0 for k in alist}
    total = len(alist)
    for i in alist:
        probdict[i]+=1
    for i in probdict:
        probdict[i] /= total
    return probdict

def sample_word(dictionary):
    p0 = np.random.random()
    cumulative = 0
    for key, value in dictionary.items():
        cumulative += value
        if p0 < cumulative:
            return key

class markov_model:
    def __init__(self, alistOfLists = [], deg = 2):
        self.instances = alistOfLists 
        if deg > 1:
            self.deg = deg
        else:
            print('deg must be greater than 1, cannot be ', deg)
        self.firsts = {} #first item of chain
        self.chains = {x:{} for x in tuple(range(1,self.deg+1))} #dictionary of dictionaries of chains (prev):{next1:%, next2:%...}
        lemm = WordNetLemmatizer()
# https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
#for lemmatizing each text correctly
        for i in self.instances:
            i = i[0].replace('/n', '')
            i = nltk.word_tokenize(i)
            for j in i:
                j = lemm.lemmatize(j,'n')
                j = lemm.lemmatize(j,'a')
                j = lemm.lemmatize(j,'v')
            # print(i)
            if len(i) == 0:
                continue
            if i[0] not in self.firsts:
                self.firsts[i[0]] = 0
            self.firsts[i[0]] += 1

            for j in range(1, self.deg): #define ngrams (prev):next
                for k in range(len(i)-j):
                    prev = []
                    for l in range(j):
                        prev.append(i[k+l])
                    if tuple(prev) not in self.chains[j]:
                        self.chains[j][tuple(prev)] = []
                    self.chains[j][tuple(prev)].append(i[k+j])

        #convert dictionary next to probability
        for i in self.firsts:
            self.firsts[i] /= len(self.firsts)

        for i in self.chains:
            for j in self.chains[i]:
                self.chains[i][j] = list2probdict(self.chains[i][j])

    def chain(self): #creates markov chain for up to degree
        sentence = []
        word0 = sample_word(self.firsts)
        sentence.append(word0)
        key = []
        word1 = ''
        for i in range(1,self.deg):
            key.append(sentence[i-1])
            while tuple(key) not in self.chains[i]:
                key.pop(0)
                i -= 1
            word1 = sample_word(self.chains[i][tuple(key)])
            sentence.append(word1)
        while word1 != '.':
            order = self.deg - 1
            key = sentence[-order:]
            while tuple(key) not in self.chains[order]:
                key.pop(0)
                order -= 1

            word1 = sample_word(self.chains[order][tuple(key)])
            id = word1.find('/n')
            if id != -1: #assuming /n always at the start of a word
                word2 = '/n'
                word3 = word1[2:]
                sentence.append(word2)
                sentence.append(word3)
            else:
                sentence.append(word1)
        return sentence
            


# %%
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

def make_path_appropriate(line):
    for i in ['*', '.', '\"', '/', '\\', '[', ']', ':', ';', '|', ',','?']:
        line = line.replace(i, '_')
    return line

def drawline(pos, text, font, draw):
    limit = 25
    offset = 15
    tokens = nltk.word_tokenize(text)
    line = ''
    for i in range(len(tokens)):
        line += ' ' + tokens[i]
        if len(line)>limit or i == len(tokens)-1:
            draw.text(xy=pos, text = line, font = font)            
            line = ' '
            pos[1] += offset
    return draw

def makememe(label):
    if '?' in label:
        line1, line2 = label.split('?',1)
    else:
        line1 = label
        line2 = ''
    line1 += '?'
    
    template = r"Z:\sibroot\repo\personal\AIMemeGenerator\meme templates\220px-Gene_Wilder_as_Willy_Wonka.jpeg"
    font = ImageFont.truetype('impact.ttf', size=15)
    im = Image.open(template)
    draw = ImageDraw.Draw(im)
    xy1 = [0,0]
    xy2 = [0,130]
    
    draw = drawline(xy1, line1, font, draw)
    draw = drawline(xy2, line2, font, draw)
    folder = os.path.join(r"meme outputs",'WillyWonka')
    if not os.path.exists(folder):
        os.mkdir(folder)
    output = str(hash(line1+line2))
    output = os.path.join(folder, output+'.jpeg')
    print(line1)
    print(line2)
    print(output)
    print()
    im.show()
    im = im.save(output,format = 'jpeg')

# %% [markdown]
# # Result: Setting n = 5 gives coherent phrases that is very similar to original memes due to small dataset

# %%
def simp_prompt_replacer(prompt, mm, deg):
    pos_prompt = nltk.pos_tag(nltk.word_tokenize(prompt))
    found = -1
    while found < 0:
        line1, line2, label = makelabel(mm,4)
        while '?' not in label:
            line1, line2, label = makelabel(mm,4)            
        pos_tag = nltk.pos_tag(nltk.word_tokenize(label))
        words, pos_tag = list(zip(*pos_tag))
        if pos_prompt[0][1] in pos_tag:
            found = list(pos_tag).index(pos_prompt[0][1])
            words = list(words)
            words[found] = pos_prompt[0][0]
            label = nltk.tokenize.treebank.TreebankWordDetokenizer().detokenize(words)
    print(label)
    return label


# %%
# deg = input('input 1-5, 1 = wack memes, 5 = civilized memes')
# deg = int(deg)
# prompt = input('enter your prompt')
# # prompt = 'father'
# mm = markov_model(labels, deg)
# label = simp_prompt_replacer(prompt, mm, deg)
# makememe(label)


# %%



