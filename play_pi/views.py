from gmusicapi import Webclient

from django.shortcuts import render_to_response
from django.template import RequestContext

from play_pi import settings
from play_pi.models import *

import logging
logger = logging.getLogger('play_pi')

def home(request):
	if settings.GPLAY_USER == "" or settings.GPLAY_PASS == "":
		return render_to_response('error.html', context_instance=RequestContext(request))

	artists = Artist.objects.all().order_by('name')

	return render_to_response('index.html',
		{'list': artists, 'view':'artist'},
		context_instance=RequestContext(request))

def artist(request,artist_id):
	artist = Artist.objects.get(id=artist_id)
	albums = Album.objects.filter(artist=artist)

	return render_to_response('index.html',
		{'list': albums, 'view':'album', 'name': artist.name },
		context_instance=RequestContext(request))

def album(request,album_id):
	album = Album.objects.get(id=album_id)
	tracks = Track.objects.filter(album=album)

	return render_to_response('album.html',
		{'album': album, 'tracks': tracks},
		context_instance=RequestContext(request))
