from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from gmusicapi import Mobileclient, Webclient
from play_pi.settings import GPLAY_USER, GPLAY_PASS
from play_pi.models import *

class Command(BaseCommand):
    help = 'Initializes the database with your Google Music library'

    def handle(self, *args, **options):
        if GPLAY_PASS == "" or GPLAY_USER == "":
            self.stdout.write('Credentials not set up. Please edit settings.py')
            return

        api = Mobileclient()
        if not api.login(GPLAY_USER,GPLAY_PASS):
            self.stdout.write('Incorrect credentials, login failed')
            return

        self.stdout.write('Connected to Google Music, downloading data...')
        library = []
        #library = api.get_all_songs()
        self.stdout.write('Data downloaded!')
        self.stdout.write('Clearing DB...')
        cursor = connection.cursor()
        # This can take a long time using ORM commands on the Pi, so lets Truncate
        #cursor.execute('DELETE FROM ' + Track._meta.db_table)
        #cursor.execute('DELETE FROM ' + Album._meta.db_table)
        #cursor.execute('DELETE FROM ' + Artist._meta.db_table)
        #cursor.execute('DELETE FROM ' + Playlist._meta.db_table)
        #cursor.execute('DELETE FROM ' + PlaylistConnection._meta.db_table)
        self.stdout.write('Parsing new data...')

        # Easier to keep track of who we've seen like this...
        artists = []
        albums = []

        for song in library:
            track = Track()

            if song['albumArtist'] == "":
                if song['artist'] == "":
                    a = "Unknown Artist"
                else:
                    a = song['artist']
            else:
                a = song['albumArtist']

            if a not in artists:
                artist = Artist()
                artist.name = a
                
                try:
                    artist.art_url = song['artistArtRef'][0]['url']
                except:
                    artist.art_url = ""
                
                artist.save()
                artists.append(a)
                self.stdout.write('Added artist: ' + a)
            else:
                artist = Artist.objects.get(name=a)
            track.artist = artist

            if song['album'] + a not in albums:
                album = Album()
                album.name = song['album']
                album.artist = artist
                try:
                    album.year = song['year']
                except:
                    pass
               
                try:
                    album.art_url = song['albumArtRef'][0]['url']
                except:
                    album.art_url = ""
                    
                album.save()
                albums.append(song['album'] + a)
            else:
                album = Album.objects.get(name=song['album'], artist=artist)
            track.album = album

            track.name = song['title']
            track.stream_id = song['id']
            try:
                track.track_no = song['trackNumber']
            except:
                track.track_no = 0
            track.save()

        self.stdout.write('All tracks saved!')
        self.stdout.write('Getting Playlists...')
        
        #playlists = api.get_all_playlists()
        self.stdout.write('Saving playlists...')
        #for playlist in playlists:
        #    p = Playlist()
        #    p.pid = playlist['id']
        #    p.name = playlist['name']
        #    p.save()

        #for playlist in Playlist.objects.all():
        self.stdout.write('Getting playlist contents.')
        playlists = api.get_all_user_playlist_contents()
        for playlist in playlists:
            p = Playlist()
            p.pid = playlist['id']
            p.name = playlist['name']
            p.save()
            for entry in playlist['tracks']:
                try:
                    track = Track.objects.get(stream_id=entry['trackId'])
                    pc = PlaylistConnection()
                    pc.playlist = p
                    pc.track = track
                    pc.save()
                except Exception:
                    print "Not found."
            #try:
            #    track = Track.objects.get(stream_id=song['id'])
            #except Exception:
            #    self.stdout.write('Couldnt find '+ song['name'])
            #    continue
            #pc = PlaylistConnection()
            #pc.playlist = Playlist.objects.get(pid=song['playlistId']) #playlist
            #pc.track = track
            #pc.save()

        self.stdout.write('Library saved!')
