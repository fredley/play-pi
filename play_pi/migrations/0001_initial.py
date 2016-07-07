# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('year', models.IntegerField(default=0)),
                ('art_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('art_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('pid', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistConnection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('playlist', models.ForeignKey(to='play_pi.Playlist')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('stream_id', models.CharField(max_length=100)),
                ('track_no', models.IntegerField(default=0)),
                ('mpd_id', models.IntegerField(default=0)),
                ('album', models.ForeignKey(to='play_pi.Album')),
                ('artist', models.ForeignKey(to='play_pi.Artist')),
            ],
        ),
        migrations.AddField(
            model_name='playlistconnection',
            name='track',
            field=models.ForeignKey(to='play_pi.Track'),
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(to='play_pi.Artist'),
        ),
        migrations.AlterUniqueTogether(
            name='album',
            unique_together=set([('name', 'artist')]),
        ),
    ]
