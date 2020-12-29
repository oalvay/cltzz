# -*- coding: utf-8 -*-
"""
@author: oalvay, 78182
"""

from multiprocessing import Pool
import requests, re, time, pickle
from bs4 import BeautifulSoup

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
    
    example = requests.get(f"https://api.genius.com/songs/{song_id}",
                                     headers=headers).json()
    print('code:', example['meta']['status'], ', id:',song_id)
    if example['meta']['status'] != 200:
        return None
    song = example['response']['song']
        
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
    

    html = BeautifulSoup(
        requests.get(song['url'], headers=headers).text,
        "html.parser"
    )

    # fork from https://github.com/johnwmillr/LyricsGenius
    # Determine the class of the div
    div = html.find("div", class_=re.compile("^lyrics$|Lyrics__Root"))
    lyrics = re.sub("[\s]+", " ", div.get_text(" "))
    return (song_id.__str__(), *info, lyrics+"\n")
        
if __name__ == '__main__':
    start = time.time()
    with open("data.csv", "w") as f:
        f.write("\t".join(['title', 'song_art_image_thumbnail_url',
                       'album_name', 'album_cover_art_url', 'release_date',
                       'primary_artist_name', 'producer_artists_name',
                       'writer_artists_name', 'stats_pageviews', 
                       'stats_hot', 'youtube_url', 'lyrics'])+"\n")
        
    
    def call_api(song_id):
        with open("data.csv", "a") as f:
            t = get_song(song_id)
            if t != None:
                f.write("\t".join(t))

    with Pool(16) as p:
        p.map(call_api,range(100))
    duration = time.time() - start
    print("time used:", duration)