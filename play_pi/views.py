from gmusicapi import Webclient
import mpd

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext

from play_pi import settings
from play_pi.models import *
from play_pi.settings import GPLAY_USER, GPLAY_PASS

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
	tracks = Track.objects.filter(album=album).order_by('track_no')

	return render_to_response('album.html',
		{'album': album, 'tracks': tracks},
		context_instance=RequestContext(request))

def play_album(request,album_id):
	album = Album.objects.get(id=album_id)
	tracks = Track.objects.filter(album=album).order_by('track_no')

	try:
		client = mpd.MPDClient()
		client.connect("localhost", 6600)
		client.clear()
		for track in tracks:
			client.add('http://0.0.0.0:8080/get_stream/' + str(track.id) + '/')
		client.play()
		client.disconnect()
	except:
		logger.debug('something went wrong!')
		pass

	return HttpResponseRedirect(reverse('album',args=[album.id,]))

def play_artist(request,artist):
	artist = Artist.objects.get(id=artist_id)
	albums = Album.objects.filter(artist=artist)

	try:
		client = mpd.MPDClient()
		client.connect("localhost", 6600)
		client.clear()
		for album in albums:
			tracks = Track.objects.filter(album=album).order_by('track_no')
			for track in tracks:
				client.add('http://0.0.0.0:8080/get_stream/' + str(track.id) + '/')
		client.play()
		client.disconnect()
	except:
		logger.debug('something went wrong!')
		pass

	return HttpResponseRedirect(reverse('artist',args=[artist.id,]))

def get_stream(request,track_id):
	track = Track.objects.get(id=track_id)
	api = Webclient()
	api.login(GPLAY_USER,GPLAY_PASS)
	url = api.get_stream_urls(track.stream_id)[0]
	return HttpResponseRedirect(url)

def play_track(request,track_id):
	track = Track.objects.get(id=track_id)
	api = Webclient()
	api.login(GPLAY_USER,GPLAY_PASS)
	url = api.get_stream_urls(track.stream_id)[0]

	try:
		client = mpd.MPDClient()
		client.connect("localhost", 6600)
		client.clear()
		client.add(url)
		client.play()
		client.disconnect()
	except:
		pass
	return HttpResponseRedirect(reverse('album',args=track.album.id))

def stop(request):
    try:
        client = mpd.MPDClient()
        client.connect("localhost", 6600)
        client.clear()
        client.stop()
        client.disconnect()
    except:
        pass

    return HttpResponseRedirect(reverse('home'))
