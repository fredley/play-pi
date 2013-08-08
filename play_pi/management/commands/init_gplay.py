from django.core.management.base import BaseCommand, CommandError

from gmusicapi import Webclient
from play_pi.settings import GPLAY_USER, GPLAY_PASS
from play_pi.models import *

class Command(BaseCommand):
    help = 'Initializes the database with your Google Music library'

    def handle(self, *args, **options):
        if GPLAY_PASS == "" or GPLAY_USER == "":
            self.stdout.write('Credentials not set up. Please edit settings.py')
            return

        api = Webclient()
        if not api.login(GPLAY_USER,GPLAY_PASS):
            self.stdout.write('Incorrect credentials, login failed')
            return

        self.stdout.write('Connected to Google Music, downloading data...')
        library = api.get_all_songs()
        self.stdout.write('Data downloaded!')
        self.stdout.write('Clearing DB...')
        for track in Track.objects.all():
            track.delete()
        for album in Album.objects.all():
            album.delete()
        for artist in Artist.objects.all():
            artist.delete()
        self.stdout.write('Parsing new data...')

        # Easier to keep track of who we've seen like this...
        artists = []
        albums = []

        for song in library:
            track = Track()

            if song['albumArtist'] not in artists:
                artist = Artist()
                artist.name = song['albumArtist']
                try:
                    artist.art_url = song['artistImageBaseUrl']
                except:
                    artist.art_url = ""
                artist.save()
                artists.append(song['albumArtist'])
                self.stdout.write('Added artist: '+song['albumArtist'])
            else:
                artist = Artist.objects.get(name=song['albumArtist'])
            track.artist = artist

            if song['album'] not in albums:
                album = Album()
                album.name = song['album']
                album.artist = artist
                try:
                    album.art_url = song['albumArtUrl']
                except:
                    album.art_url = ""
                album.save()
                albums.append(song['album'])
            else:
                album = Album.objects.get(name=song['album'])
            track.album = album

            track.name = song['title']
            track.stream_id = song['id']
            try:
                track.track_no = song['track']
            except:
                track.track_no = 0
            track.save()
