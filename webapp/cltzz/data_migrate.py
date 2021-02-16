from datetime import date
from engine.models import Song
import pandas as pd
import numpy as np

df = pd.read_csv('data_3000000_4000000.csv', sep = "\t",
        error_bad_lines=False, warn_bad_lines=False, na_values = "_")

for col in df.columns:
    if col == 'release_date':
        df.loc[df[col].isna(), col] = '2000-01-01'
        df[col] = df[col].map(date.fromisoformat)
    elif col == 'stats_pageviews':
        df.loc[df[col].isna(), col] = -1
        df[col] = df[col].astype(int)
    elif df[col].dtype == 'O':
        df.loc[df[col].isna(), col] = 'no_' + col

for i in range(len(df)):
    temp = Song(**df.iloc[i,].to_dict())
    temp.id = temp['api_id']
    temp.save()


