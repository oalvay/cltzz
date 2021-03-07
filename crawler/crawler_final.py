# -*- coding: utf-8 -*-
"""
@author: oalvay, 78182
"""

from multiprocessing import Pool
import requests, re, time, pickle
from bs4 import BeautifulSoup
from sys import argv, exit
from requests.exceptions import ConnectionError, Timeout
import pandas as pd

headers = {'Authorization':
           'Bearer NxudGFdc5dNGFgFn07XO9BMe7Gz0k6wAtQ9PkvX1dQC9FduLKMJYL7gnKLyZrQpf'}
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

def get_song(song_id):
    
    count = 0
    try:
        example = requests.get(f"https://api.genius.com/songs/{song_id}", headers=headers, timeout = 5)

        while example.status_code in [429, 500, 502, 503, 504] and count < 5:
            time2sleep = 4000
            if example.status_code == 429:
                time2sleep = int(example.headers['Retry-After']) + 100
            # elif example.status_code == 403:
            #     time2sleep = 10
            print(f"sleeping, awake after {time2sleep}s")
            count += 1
            time.sleep(time2sleep)
            print('retry: code:', example.status_code, example.reason, ', id:',song_id)
            example = requests.get(f"https://api.genius.com/songs/{song_id}", headers=headers,  timeout = 5)

        if example.status_code != 200:
            print('code:', example.status_code, example.reason, ', id:',song_id)
            return None

        try:
            song = example.json()['response']['song']
        except ValueError:
            return None

        apple_music_id = get_attribute(song, 'apple_music_id')
        if apple_music_id == '_':
            return None
        medias = get_attribute(song, 'media')
        youtube_url = "_"
        if medias:
            for media in medias:
                if media['provider'] == 'youtube':
                    youtube_url = media['url']
                    break
        info = [get_attribute(song, 'title'),
                apple_music_id,
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

        lyrics_example = requests.get(song['url'], headers=headers, timeout=5)

        if lyrics_example.status_code != 200:
            print('lyrics code:', lyrics_example.status_code, ', id:',song_id)
            return None
        html = BeautifulSoup(lyrics_example.text, "html.parser")

        # fork from https://github.com/johnwmillr/LyricsGenius
        # Determine the class of the div
        div = html.find("div", class_=re.compile("^lyrics$|Lyrics__Root"))
        if div is None:
            lyrics = ' [Instrumental] \n'
        else:
            lyrics = re.sub("[\s]+", " ", div.get_text(" "))
        return (song_id.__str__(), *info, lyrics+"\n")
    except Timeout as e:
        print(f"id:{song_id}, Timeout: retry after 5 seconds")
        time.sleep(5)
    except ConnectionError as e:
        print(f"id:{song_id}, ConnectionError: retry after 5 mins")
        time.sleep(300)
        return get_song(song_id)
    except Exception as e:
        print(f"id:{song_id}, Error: {e}, sleeping")
        time.sleep(4000)
        return get_song(song_id)
    
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

    tried = set()
    try:
        data = pd.read_csv(filename, error_bad_lines=False,
                        warn_bad_lines=False, na_values = "_", sep="\t",
                        usecols=['api_id'])
        tried = set(data.api_id.to_list())
        del data
    except FileNotFoundError:
        with open(filename, "w") as f:
            f.write("\t".join(['api_id', 'title', 'apple_music_id', 'song_art_image_thumbnail_url',
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
        p.map(call_api, tuple(set(range(*id_range)) - tried))
    duration = time.time() - start
    print("time used:", duration)