from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.index, name='index'),
    path('search', views.search, name='search'),
    path('advanced', views.advanced, name='advanced'),
    path('detail', views.detail, name='detail'),
]

