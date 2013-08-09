from gmusicapi import Webclient
import mpd
from django.core.cache import cache

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from play_pi.models import *
from play_pi.settings import GPLAY_USER, GPLAY_PASS

import logging
logger = logging.getLogger('play_pi')

api = Webclient()
api.login(GPLAY_USER,GPLAY_PASS)

client = mpd.MPDClient()
client.connect("localhost", 6600)

def home(request):
	if GPLAY_USER == "" or GPLAY_PASS == "":
		return render_to_response('error.html', context_instance=RequestContext(request))

	artists = Artist.objects.all().order_by('name')

	return render_to_response('index.html',
		{'list': artists, 'view':'artist'},
		context_instance=RequestContext(request))

def artist(request,artist_id):
	artist = Artist.objects.get(id=artist_id)
	albums = Album.objects.filter(artist=artist)

	return render_to_response('index.html',
		{'list': albums, 'view':'album', 'artist': artist},
		context_instance=RequestContext(request))

def playlists(request):
	playlists = Playlist.objects.all()
	return render_to_response('index.html',
		{'list': playlists, 'view':'playlist'},
		context_instance=RequestContext(request))

def playlist(request,playlist_id):
	playlist = Playlist.objects.get(id=playlist_id)
	tracks = [pc.track for pc in PlaylistConnection.objects.filter(playlist=playlist)]
	return render_to_response('playlist.html',
		{'playlist': playlist, 'tracks': tracks},
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
	urls = []
	for track in tracks:
		urls.append('http://0.0.0.0:8080/get_stream/' + str(track.id) + '/')
	mpd_play(urls)

	return HttpResponseRedirect(reverse('album',args=[album.id,]))

def play_artist(request,artist_id):
	artist = Artist.objects.get(id=artist_id)
	albums = Album.objects.filter(artist=artist)
	urls = []
	for album in albums:
		tracks = Track.objects.filter(album=album).order_by('track_no')
		for track in tracks:
			urls.append('http://0.0.0.0:8080/get_stream/' + str(track.id) + '/')
	mpd_play(urls)
	return HttpResponseRedirect(reverse('artist',args=[artist.id,]))

def play_playlist(request,playlist_id):
	playlist = Playlist.objects.get(id=playlist_id)
	tracks = [pc.track for pc in PlaylistConnection.objects.filter(playlist=playlist)]
	urls = []
	for track in tracks:
		urls.append('http://0.0.0.0:8080/get_stream/' + str(track.id) + '/')
	mpd_play(urls)
	return HttpResponseRedirect(reverse('playlist',args=[playlist.id,]))

def get_stream(request,track_id):
	track = Track.objects.get(id=track_id)
	url = get_gplay_url(track.stream_id)
	return HttpResponseRedirect(url)

def play_track(request,track_id):
	track = Track.objects.get(id=track_id)
	url = get_gplay_url(track.stream_id)
	mpd_play([url,])
	return HttpResponseRedirect(reverse('album',args=track.album.id))

def stop(request):
	client = get_client()
	client.clear()
	client.stop()
	return HttpResponseRedirect(reverse('home'))

def random(request):
	client = get_client()
	status = client.status()
	client.random( (-1 * int(status['random'])) + 1 )
	return HttpResponseRedirect(reverse('home'))

def repeat(request):
	client = get_client()
	status = client.status()
	client.repeat( (-1 * int(status['repeat'])) + 1 )
	logger.debug(status)
	return HttpResponseRedirect(reverse('home'))

def ajax(request,method):
	client = get_client()
	status = client.status()
	if method == 'random':
		client.random( (-1 * int(status['random'])) + 1 )
	elif method == 'repeat':
		client.repeat( (-1 * int(status['repeat'])) + 1 )
	elif method == 'stop':
		client.stop()
	return_data = client.status()
	return HttpResponse(simplejson.dumps(return_data), 'application/javascript')

def get_gplay_url(stream_id):
	global api
	try:
		url = api.get_stream_urls(stream_id)[0]
	except:
		api.login(GPLAY_USER,GPLAY_PASS)
		url = api.get_stream_urls(stream_id)[0]
	return url

def mpd_play(urls):
	client = get_client()
	client.clear()
	for url in urls:
		client.add(url)
	client.play()

def get_client():
	global client
	try:
		client.status()
	except:
		client.connect("localhost", 6600)
	return client
