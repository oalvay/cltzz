
from multiprocessing import Process, Manager, Pool
from concurrent.futures import ProcessPoolExecutor

def call_api(managed_list,song_id):
    t = get_song(song_id)
    if t != None:
        managed_list.append(t)
    print('job finished, id:',song_id)
    
if __name__ == '__main__':
    manager = Manager()
    managed_l = manager.list()
    
    with Pool(8) as p:
        p.map(call_api,{managed_l,range(1000)})
    
    
        



import requests, json, re

from bs4 import BeautifulSoup

headers={'Authorization':
         'Bearer NxudGFdc5dNGFgFn07XO9BMe7Gz0k6wAtQ9PkvX1dQC9FduLKMJYL7gnKLyZrQpf'}

def get_song(song_id):
    example = json.loads(requests.get(f"https://api.genius.com/songs/{song_id}",
                                     headers=headers).text)
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
    lyrics = div.get_text()
    
    return artist,album_name,song_name,lyrics