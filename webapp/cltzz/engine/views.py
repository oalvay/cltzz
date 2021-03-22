from django.shortcuts import render
from django.http import HttpResponse
from .models import Song
from .utils.retrieve import *
from json import dumps as jdumps
from time import time as ttime

import requests, re
from bs4 import BeautifulSoup

headers = {'Authorization':
           'Bearer NxudGFdc5dNGFgFn07XO9BMe7Gz0k6wAtQ9PkvX1dQC9FduLKMJYL7gnKLyZrQpf'}

def index(request):
    return render(request, 'engine/index.html')

def result(request):
    return render(request, 'engine/result.html')

# def detail(request):
#     return render(request, 'engine/detail.html')

def search(request):
    start_time = ttime()
    query = request.GET.get('query')
    matched_docs, clean_query = retrieve(query, docs_num=250)
    selected_docs = []
    titles = []
    lyricses = []
    pageviews = []
    for song_id in matched_docs:
        a = Song.objects.get(pk = song_id)
        selected_docs.append(song_id)
        titles.append(clean_title(a.title))
        lyricses.append(tokenize(a.lyrics[0:400])[:10])
        pageviews.append(a.stats_pageviews)

        # if two songs have the same title, remove the one with less
        # pageviews
        if titles[-1] in titles[:-1]:
            same_title_song = titles[:-1].index(titles[-1])
            if pageviews[same_title_song] <= pageviews[-1]:
                selected_docs.pop(same_title_song)
                titles.pop(same_title_song)
                lyricses.pop(same_title_song)
                pageviews.pop(same_title_song)
            else:
                selected_docs.pop()
                titles.pop()
                lyricses.pop()
                pageviews.pop()

        # the same applied to lyrics
        if lyricses[-1] in lyricses[:-1]:
            same_lyrics_song = lyricses[:-1].index(lyricses[-1])
            if pageviews[same_title_song] <= pageviews[-1]:
                selected_docs.pop(same_lyrics_song)
                titles.pop(same_lyrics_song)
                lyricses.pop(same_lyrics_song)
                pageviews.pop(same_title_song)
            else:
                selected_docs.pop()
                titles.pop()
                lyricses.pop()
                pageviews.pop()

        if len(selected_docs) >= 50:
            break

    ranked_docs = rerank(selected_docs, clean_query, bert = True)

    results = []
    for song_id in ranked_docs:
        a = Song.objects.get(pk = song_id)
        song = {}
        song['title']= a.title
        song['pageviews'] = a.stats_pageviews
        song['artist'] = a.primary_artist_name
        song['abstract']=a.lyrics[0:400]
        song['id'] = str(song_id)
        results.append(song)

    resp = {'err': 'false', 'detail': 'Get success','exe_time':ttime() - start_time, 'query': query, 'ret': results}
    return HttpResponse(jdumps(resp), content_type="application/json")

def detail(request):
    id = request.GET.get('id')
    doc_id = int(id)
    a = Song.objects.get(pk=doc_id)
    song = {}
    song['title']= a.title
    song['image_url']= a.song_art_image_thumbnail_url
    song['artist'] = a.primary_artist_name
    song['album']=a.album_name
    song['youtube_url'] = a.youtube_url

    try:
        api_info = requests.get(f"https://api.genius.com/songs/{a.api_id}",\
                     headers=headers, timeout = 5)
        if api_info.status_code != 200:
            1 / 0
        else:
            lyrics_url = api_info.json()['response']['song']['url']
            lyrics_info = requests.get(lyrics_url, headers=headers, timeout=5)
            if lyrics_info.status_code != 200:
                1 / 0
            else:
                html = BeautifulSoup(lyrics_info.text, "html.parser")
                div = html.find("div", class_=re.compile("^lyrics$|Lyrics__Root"))
                song['lyrics']= re.sub("\n+", "\n", div.get_text("\n"))
    except:
        song['lyrics']= a.lyrics


    resp = {'err': 'false', 'detail': 'Get success', 'ret': song}
    return HttpResponse(jdumps(resp), content_type="application/json")
