import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import string, re, pickle, gc
from tqdm import tqdm

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

files = []

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        files.append(os.path.join(dirname, filename))

def isEnglish(s):
    return sum([ord(i)<128 for i in s]) / len(s) > 0.99 and len(s) > 5

def tokenize(text):
    text = re.sub(r'(www|http)\S+', '', text.lower())
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.translate(str.maketrans('', '', string.digits))
    return text.split()

df = pd.concat([pd.read_csv(
    datafile, sep = "\t", error_bad_lines=False, warn_bad_lines=False, na_values = "_")
                for datafile in files]
)

num = df.api_id.map(lambda x: type(x) is int or str.isdigit(x))

df = df.loc[num]

df['api_id'] = df.api_id.astype('int')
df['lyrics'] = df.lyrics.astype('str')

df = df.loc[df.lyrics.map(isEnglish)]

df.to_csv("filtered.csv")