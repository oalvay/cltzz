from datetime import date
from engine.models import Song
import pandas as pd
from tqdm import tqdm
import pickle

with open("docs_id.pkl", 'rb') as f:
    docs_id = pickle.load(f)
    
docs_id_dict = {doc_id:idx for idx, doc_id in enumerate(docs_id)}

df = pd.read_csv('filtered.csv')
df = df.drop(["Unnamed: 0"], axis = 1)

def is_date(x):
	return len(x.split('-')) == 3

def is_num(x):
    try:
        int(x)
        return True
    except:
        return False

def is_bool(x):
    return type(x) == bool

for col in df.columns:
    if col == 'release_date':
        df.loc[df[col].isna(), col] = '2000-01-01'
        df = df.loc[df[col].map(is_date)]
        df[col] = df[col].map(date.fromisoformat)
    elif col == 'stats_pageviews':
        df.loc[df[col].isna(), col] = '0'
        df = df.loc[df[col].map(is_num)]
        df[col] = df[col].astype(int)
    elif col == 'stats_hot':
        df.loc[df[col].isna(), col] = False
        df = df.loc[df[col].map(is_bool)]
        df[col] = df[col].astype(bool)
    elif col == 'apple_music_id':
        df[col] = df[col].astype(str)
    elif df[col].dtype == 'O':
        df.loc[df[col].isna(), col] = 'no_' + col

#batch = []

for i in tqdm(range(len(df))):
    # if i % 1000:
    #     Song.objects.bulk_create(batch)
    #     del batch
    #     batch = []
    temp = df.iloc[i,].to_dict()
    #temp['id'] =docs_id_dict[temp['api_id']]
    #batch.append(Song(**temp))
    #Song.objects.create(**temp)
    temp2 = Song(**temp)
    temp2.id = docs_id_dict[temp['api_id']]
    temp2.save()
    del temp, temp2

#Song.objects.bulk_create(batch)

