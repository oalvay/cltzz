from django.shortcuts import render
from django.http import HttpResponse
from .models import Song
from .utils.retrieve import *
from json import dumps as jdumps


def index(request):
    return render(request, 'engine/index.html')

def result(request):
    return render(request, 'engine/result.html')

def detail(request):
    return render(request, 'engine/detail.html')

def search(request):
    query = request.GET.get('query')
    matched_docs, exe_time = retrieve(query, docs_num=50)
    results = []
    for song_id in matched_docs:
        a = Song.objects.get(pk = song_id)
        song = {}
        song['title']= a.title
        song['abstract']=a.lyrics[0:400]
        song['artist'] = a.primary_artist_name
        song['id'] = a.api_id
        results.append(song)
    resp = {'err': 'false', 'detail': 'Get success','exe_time':exe_time, 'query': query, 'ret': results}
    return HttpResponse(jdumps(resp), content_type="application/json")

def detail(request):
    id = request.GET.get('id')
    a = Song.objects.get(pk=id)
    song = {}
    song['title']= a.title
    song['lyrics']= a.lyrics
    song['image_url']= a.song_art_image_thumbnail_url
    song['artist'] = a.primary_artist_name
    song['album']=a.album_name
    resp = {'err': 'false', 'detail': 'Get success', 'ret': song}
    return HttpResponse(jdumps(resp), content_type="application/json")
