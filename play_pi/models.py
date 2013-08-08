from django.db import models


class Artist(models.Model):
	name = models.CharField(max_length=200, unique=True)
	art_url = models.CharField(max_length=200)


class Album(models.Model):
	name = models.CharField(max_length=200, unique=True)
	art_url = models.CharField(max_length=200)
	artist = models.ForeignKey(Artist)


class Track(models.Model):
	name = models.CharField(max_length=200)
	artist = models.ForeignKey(Artist)
	album = models.ForeignKey(Album)
	stream_id = models.CharField(max_length=100)
	track_no = models.IntegerField(default=0)


class Playlist(models.Model):
	name = models.CharField(max_length=200)
	pid = models.CharField(max_length=200)

	def get_art(self):
		pc = PlaylistConnection.objects.filter(playlist=self)[0]
		track = pc.track
		artist = track.artist
		return artist.art_url

	art_url = property(get_art)


class PlaylistConnection(models.Model):
	track = models.ForeignKey(Track)
	playlist = models.ForeignKey(Playlist)
