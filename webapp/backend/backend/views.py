from django.http import HttpResponse
from .models import Song
import json


def search(request):

    def search(query):
        return [3000012, 3000165, 3000173]
    song_ids = search('ss')
    for song_id in song_ids:
         a = Song.objects.get(pk = song_id)

    query = request.GET.get('query')
    print(query)
    result = [
        {'title': 'Something Just Like This',
         'abstract': 'I\'ve been reading books of old The legends and the myths Achilles and his gold Hercules and his gifts Spider-Man\'s control And Batman with his fists And clearly I don\'t see myself upon that list But she said, where\'d you wanna go? How much you'},
        {'title': 'Roxanne',
         'abstract': 'Roxanne You don\'t have to put on the red light Those days are over You don\'t have to sell your body to the night Roxanne You don\'t have to wear that dress tonight Walk the streets for money You don\'t care if it\'s wrong or if it\'s right Roxanne You don\'t have to put on the red light Roxanne You don\'t have to put on the red light Roxanne (Put on the red light)'},
        {'title': '一路向北',
         'abstract': '後視鏡裡的世界 越來越遠的道別 你轉身向北 側臉還是很美 我用眼光去追 竟聽見你的淚 在車窗外面徘徊 是我錯失的機會 你站的方位 跟我中間隔著淚 街景一直在後退 你的崩潰在窗外零碎 我一路向北 離開有你的季節'}];
    resp = {'err': 'false', 'detail': 'Get success', 'ret': result}
    return HttpResponse(json.dumps(resp), content_type="application/json")
