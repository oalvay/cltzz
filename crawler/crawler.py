# -*- coding: utf-8 -*-
"""
@author: oalvay, 78182
"""

from multiprocessing import Pool, Manager
import requests, re, time, pickle
from bs4 import BeautifulSoup

headers = {'Authorization':
           'Bearer NxudGFdc5dNGFgFn07XO9BMe7Gz0k6wAtQ9PkvX1dQC9FduLKMJYL7gnKLyZrQpf'}

def get_song(song_id):
    example = requests.get(f"https://api.genius.com/songs/{song_id}",
                                     headers=headers).json()
    print('code:', example['meta']['status'], ', id:',song_id)
    if example['meta']['status'] != 200:
        return None
    song = example['response']['song']
        
    artist = song['primary_artist']['name']
    if(song['album'] == None):
        album_name = 'No Album'
    else:
        album_name = song['album']['name']
    song_name = song['title']

    song_path = example['response']['song']['path']
    html = BeautifulSoup(
        requests.get(f"https://genius.com{song_path}", headers=headers).text,
        "html.parser"
    )

    # fork from https://github.com/johnwmillr/LyricsGenius
    # Determine the class of the div
    div = html.find("div", class_=re.compile("^lyrics$|Lyrics__Root"))
    lyrics = div.get_text(" ")
    
    return song_id, artist, album_name, song_name, lyrics
    
manager = Manager()
global managed_l
managed_l= manager.list()

def call_api(song_id):
    t = get_song(song_id)
    if t != None:
        managed_l.append(t)
        
if __name__ == '__main__':
    start = time.time()
    
    with Pool(16) as p:
        p.map(call_api,range(1000))
    with open('somefile', 'wb') as f:
        pickle.dump(list(managed_l), f)
        
    duration = time.time() - start
    print("time used:", duration)