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
    docs, exe_time = retrieve(query, docs_num=10)
    results = []
    for song_id in docs:
        a = Song.objects.get(pk = song_id)
        song = {}
        song['title']= a.title
        song['abstract']=a.lyrics[0:400]
        song['artist'] = a.primary_artist_name
        song['id'] = a.api_id
        results.append(song)
    print(results)
    resp = {'err': 'false', 'detail': 'Get success', 'query': query, 'ret': results}
    return HttpResponse(jdumps(resp), content_type="application/json")
