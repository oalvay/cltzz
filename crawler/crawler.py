# -*- coding: utf-8 -*-
"""
@author: oalvay, 78182
"""

from multiprocessing import Pool
import requests, re, time, pickle
from bs4 import BeautifulSoup
from sys import argv, exit

headers = {'Authorization':
           'Bearer NxudGFdc5dNGFgFn07XO9BMe7Gz0k6wAtQ9PkvX1dQC9FduLKMJYL7gnKLyZrQpf',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
def get_attribute(obj, sth, sth_else = None):
    if sth_else == None:
        try:
            return obj[sth] if obj[sth] is not None else '_'
        except KeyError:
            return '_'
    else:
        try:
            return obj[sth][sth_else] if obj[sth][sth_else] is not None else '_'
        except (KeyError, TypeError):
            return '_'
        
def get_url(id_, url, headers):
    try:
        example = requests.get(url, headers=headers)
        return example
    except requests.exceptions.ConnectionError:
        print(f"id:{id_}, ConnectionError, sleeping")
        time.sleep(4000)
        return get_url(id_, url, headers)

def get_song(song_id):
    
    
    example = requests.get(f"https://api.genius.com/songs/{song_id}", headers=headers)
    print('code:', example.status_code, example.reason, ', id:',song_id)
    
    while example.status_code in [429, 500, 502, 503, 504]:
        time2sleep = 4000
        if example.status_code == 429:
            time2sleep = int(example.headers['Retry-After']) + 100
        print(f"sleeping, awake after {time2sleep}s")
        time.sleep(time2sleep)
        print('retry: code:', example.status_code, example.reason, ', id:',song_id)
        example = get_url(song_id, f"https://api.genius.com/songs/{song_id}", headers)
        
    if example.status_code != 200:
        return None
            
    try:
        song = example.json()['response']['song']
    except ValueError:
        return None
        
    medias = get_attribute(song, 'media')
    youtube_url = "_"
    if medias:
        for media in medias:
            if media['provider'] == 'youtube':
                youtube_url = media['url']
                break
    info = [get_attribute(song, 'title'),
        get_attribute(song, 'song_art_image_thumbnail_url'),
        get_attribute(song, 'album', 'name'),
        get_attribute(song, 'album', 'cover_art_url'),
        get_attribute(song, 'release_date'),
        get_attribute(song, 'primary_artist', 'name'),
        "_".join([artist['name'] for artist in get_attribute(song, 'producer_artists')]),
        "_".join([artist['name'] for artist in get_attribute(song, 'writer_artists')]),
        get_attribute(song, 'stats', 'pageviews').__str__(),
        get_attribute(song, 'stats', 'hot').__str__(),
        youtube_url]
    

    lyrics_example = get_url(song_id, song['url'], headers)
    
    if lyrics_example.status_code != 200:
        print('lyrics code:', lyrics_example.status_code, ', id:',song_id)
        return None
    html = BeautifulSoup(lyrics_example.text, "html.parser")

    # fork from https://github.com/johnwmillr/LyricsGenius
    # Determine the class of the div
    div = html.find("div", class_=re.compile("^lyrics$|Lyrics__Root"))
    if div is None:
        print('lyrics code:', lyrics_example.status_code, ', id:',song_id)
        return None
    lyrics = re.sub("[\s]+", " ", div.get_text(" "))
    return (song_id.__str__(), *info, lyrics+"\n")
        
if __name__ == '__main__':
    start = time.time()
    
    try:
        global id_range
        id_range = int(argv[1]), int(argv[2])
    except:
        exit('please provide two numbers as start and end ids for crawlers')
    if min(id_range) < 0 or id_range[0] - id_range[1] > 0:
        exit('make sure you provide valid range of ids')
        
#     global id_range 
#     id_range = (1000, 3000)
    filename = f"data_{id_range[0]}_{id_range[1]}.csv"
    with open(filename, "w") as f:
        f.write("\t".join(['api_id', 'title', 'song_art_image_thumbnail_url',
                       'album_name', 'album_cover_art_url', 'release_date',
                       'primary_artist_name', 'producer_artists_name',
                       'writer_artists_name', 'stats_pageviews', 
                       'stats_hot', 'youtube_url', 'lyrics'])+"\n")
        
    
    def call_api(song_id):
        with open(filename, "a") as f:
            t = get_song(song_id)
            if t != None:
                f.write("\t".join(t))

    with Pool(8) as p:
        p.map(call_api, range(*id_range))
    duration = time.time() - start
    print("time used:", duration)