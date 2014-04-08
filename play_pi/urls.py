from django.conf.urls import patterns, include, url
from django.contrib import admin
from play_pi.models import *

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'play_pi.views.home', name='home'),
	url(r'^artist/(?P<artist_id>\d+)/$', 'play_pi.views.artist', name='artist'),
	url(r'^album/(?P<album_id>\d+)/$', 'play_pi.views.album', name='album'),
	url(r'^playlists/$', 'play_pi.views.playlists', name='playlists'),
	url(r'^playlist/(?P<playlist_id>\d+)/$', 'play_pi.views.playlist', name='playlist'),
	url(r'^play/track/(?P<track_id>\d+)/$', 'play_pi.views.play_track', name='play_track'),
	url(r'^play/album/(?P<album_id>\d+)/$', 'play_pi.views.play_album', name='play_album'),
	url(r'^play/artist/(?P<artist_id>\d+)/$', 'play_pi.views.play_artist', name='play_artist'),
	url(r'^play/playlist/(?P<playlist_id>\d+)/$', 'play_pi.views.play_playlist', name='play_playlist'),
	url(r'^controls/random/$', 'play_pi.views.random', name='random'),
	url(r'^controls/repeat/$', 'play_pi.views.repeat', name='repeat'),
	url(r'^get_stream/(?P<track_id>\d+)/$', 'play_pi.views.get_stream', name='get_stream'),
	url(r'^stop/$', 'play_pi.views.stop', name='stop'),
	url(r'^ajax/(?P<method>\w+)/$', 'play_pi.views.ajax', name='ajax'),
	url(r'^admin/', include(admin.site.urls)),
)

#Startup code here because there does not seem to be a better place
Track.objects.filter(mpd_id__gt=0).update(mpd_id=0) # we have to reset the MPD_ID because MPD reuses IDs when its restarted.