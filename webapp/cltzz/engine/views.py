from django.shortcuts import render
from django.http import HttpResponse
from .models import Song
import json


def index(request):
    return render(request, 'engine/index.html')

def result(request):
    return render(request, 'engine/result.html')

def detail(request):
    return render(request, 'engine/detail.html')

def search(request):
     # query = request.POST['query']
    song_ids = [1000012, 1000165, 1000173]
    results = dict()
    for song_id in song_ids:
         a = Song.objects.get(pk = song_id)
         print(a.__dict__)
         results[a.title] = a.lyrics

    # query = request.GET.get('query')
    # print(query)
    resp = {'err': 'false', 'detail': 'Get success', 'ret': results}
    return HttpResponse(json.dumps(resp), content_type="application/json")
