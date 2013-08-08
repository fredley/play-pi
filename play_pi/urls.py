from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'play_pi.views.home', name='home'),
    url(r'^artist/(?P<artist_id>\d+)/$', 'play_pi.views.artist', name='artist'),
    url(r'^album/(?P<album_id>\d+)/$', 'play_pi.views.album', name='album'),
    url(r'^play/track/(?P<track_id>\d+)/$', 'play_pi.views.play_track', name='play_track'),
    url(r'^play/album/(?P<album_id>\d+)/$', 'play_pi.views.play_album', name='play_album'),
    url(r'^get_stream/(?P<track_id>\d+)/$', 'play_pi.views.get_stream', name='get_stream'),
    url(r'^stop/$', 'play_pi.views.stop', name='stop'),
    url(r'^admin/', include(admin.site.urls)),
)
