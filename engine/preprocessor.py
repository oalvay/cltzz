# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 20:30:29 2021

@author: siyue chen, zhendong tian, zhuocheng zheng.
"""

import pandas as pd
import string, re, pickle, gc
from tqdm import tqdm

def isEnglish(s):
    return sum([ord(i)<128 for i in s]) / len(s) > 0.99 and len(s) > 5
    
def tokenize(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\S+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.translate(str.maketrans('', '', string.digits))
    stringlist = text.split()
    return stringlist
    

datafile = 'data_1_1000000.csv'
data = pd.read_csv(
    datafile, sep = "\t", error_bad_lines=False, warn_bad_lines=False, na_values = "_",
                usecols = ["api_id", "lyrics"]
)

data['lyrics'] = data.lyrics.astype('str')

data = data.loc[data.lycris.map(isEnglish)]

data['lyrics'] = data.lycris.map(tokenize)


gc.collect()

term_dict = {}
for i in tqdm(range(len(data))):
    d_id, doc = data.iloc[i,]
    for index,t in enumerate(doc):
        if t not in term_dict:
            term_dict[t] = {}
            term_dict[t][d_id] = [index]
        elif d_id not in term_dict[t]:
            term_dict[t][d_id] = [index]
            
        else:
            term_dict[t][d_id].append(index)
            
#Saved as pickle
with open("inverted_index.pkl",'w') as f:
    pickle.dump(term_dict,f)