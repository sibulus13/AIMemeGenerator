import os
from flask import Flask
path = r'Z:\sibroot\repo\personal\AIMemeGenerator'
os.chdir(path) 
import MM_meme_generator as MM
import time


deg = input('input 1-5, 1 = wack memes, 5 = civilized memes: ')
deg = int(deg)
prompt = input('enter your prompt: ')
# prompt = 'father'
time.
mm = MM.markov_model(MM.labels, deg)
label = MM.simp_prompt_replacer(prompt, mm, deg)
MM.makememe(label)