from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'play_pi.views.home', name='home'),
    url(r'^artist/(?P<artist_id>\d+)/$', 'play_pi.views.artist', name='artist'),
    url(r'^album/(?P<album_id>\d+)/$', 'play_pi.views.album', name='album'),
    url(r'^admin/', include(admin.site.urls)),
)
