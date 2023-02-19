from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from boards import views

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    
    url(r'^$', views.home, name='home'),     # Or: path('boards/', include('boards.urls')),
    url(r'^board/(?P<pk>\d+)$', views.board_topics, name='board_topics'),
    url(r'^board/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
]
