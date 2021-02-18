from datetime import date
from engine.models import Song
import pandas as pd
from tqdm import tqdm

df = pd.read_csv('data_6000000_6450000.csv', sep = "\t",
        error_bad_lines=False, warn_bad_lines=False, na_values = "_")

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
        print('hot ok')
    elif df[col].dtype == 'O':
        df.loc[df[col].isna(), col] = 'no_' + col

for i in tqdm(range(len(df))):
    try:
        temp = df.iloc[i,].to_dict()
        temp2 = Song(**temp)
        temp2.id = temp['api_id']
        temp2.save()
        del temp
    except (TypeError, ValueError) as e:
        continue

