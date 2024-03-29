from django.db import models


class Song(models.Model):
    api_id = models.IntegerField()
    title = models.CharField(max_length=500)
    apple_music_id = models.CharField(max_length=30)
    song_art_image_thumbnail_url = models.CharField(max_length=500)
    album_name = models.CharField(max_length=250)
    album_cover_art_url = models.CharField(max_length=500)
    release_date = models.DateField()
    primary_artist_name = models.CharField(max_length=250)
    producer_artists_name = models.CharField(max_length=500)
    writer_artists_name = models.CharField(max_length=1000)
    stats_pageviews = models.IntegerField()
    stats_hot = models.BooleanField()
    youtube_url = models.CharField(max_length=200)
    lyrics = models.TextField()

# class Index(models.Model):
#     pass

# class Document(models.Model):
#     api_id = models.IntegerField(default=-1)
#     token = models.ForeignKey(Index, on_delete=models.CASCADE)
#     List = models.JSONField()