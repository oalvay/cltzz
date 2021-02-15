from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('engine/', include(('engine.urls', 'engine'), namespace = 'engine')),
    path('admin/', admin.site.urls),
]