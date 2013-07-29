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

# REFERENCE

# {u'origin': [],
#  u'rating': 0,
#  u'titleNorm': u'miserere nostri for 7 voices',
#  u'lastPlayed': 1307145646919407L,
#  u'disc': 0,
#  u'composer': u'Thomas Tallis',
#  u'year': 2001,
#  u'id': u'93632cad-305c-34fd-ac65-d267d6cb69b7',
#  u'subjectToCuration': False,
#  u'album': u'Tallis: Spem in Alium',
#  u'title': u'Miserere Nostri for 7 voices',
#  u'recentTimestamp': 1307145646910000L,
#  u'deleted': False,
#  u'albumArtist': u'Tallis',
#  u'albumArtUrl': u'//lh4.googleusercontent.com/e71g38W6mwuMrUCOfObYEj2UJ9uYKQtC3P7ZHc8f_inC0DjHUvohBo6VOSk7=s130-c-e100',
#  u'type': 2,
#  u'artistImageBaseUrl': u'//lh3.googleusercontent.com/wVfOzJNL1gefc1lAg-Pyn8mfSF8U2B-JDU3_Jx229ZHMioc-yMO_8d2bd716gOsP6nDmvAj0xw',
#  u'track': 6,
#  u'curationSuggested': False,
#  u'albumArtistNorm': u'tallis',
#  u'totalTracks': 0,
#  u'beatsPerMinute': 0,
#  u'curatedByUser': False,
#  u'genre': u'Classical',
#  u'playCount': 0,
#  u'creationDate': 1307145617283354L,
#  u'bitrate': 128,
#  u'comment': u'',
#  u'name': u'Miserere Nostri for 7 voices',
#  u'albumNorm': u'tallis: spem in alium',
#  u'artist': u'The Tallis Scholars',
#  u'url': u'',
#  u'totalDiscs': 0,
#  u'artistMatchedId': u'Aobhethbcqe2jrojpwtr4fhko5i',
#  u'durationMillis': 151949,
#  u'artistNorm': u'the tallis scholars'}
