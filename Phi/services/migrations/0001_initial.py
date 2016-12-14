# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('actor_image', models.ImageField(upload_to='media/', null=True, blank='True')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_text', models.TextField()),
                ('datetime', models.DateTimeField()),
                ('member', models.ForeignKey(to='users.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('member', models.ForeignKey(to='users.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('year', models.PositiveSmallIntegerField()),
                ('avg_rate', models.FloatField()),
                ('link_to_imdb', models.CharField(max_length=300)),
                ('total_raters', models.PositiveIntegerField()),
                ('summary', models.TextField()),
                ('genre', models.CharField(max_length=40)),
                ('initial_release', models.DateField()),
                ('director', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=40)),
                ('author', models.CharField(max_length=100)),
                ('song_writer', models.CharField(max_length=100)),
                ('cinematography', models.CharField(max_length=100)),
                ('running_time', models.PositiveSmallIntegerField()),
                ('poster_image', models.ImageField(upload_to='media/', null=True, default='media/unknown-movie.png', blank='True')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notif_type', models.CharField(max_length=20)),
                ('seen', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.PositiveSmallIntegerField()),
                ('post_text', models.TextField(max_length=500)),
                ('datetime', models.DateTimeField()),
                ('member', models.ForeignKey(to='users.Member', related_name='author')),
                ('movie', models.ForeignKey(to='services.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role_name', models.CharField(max_length=50)),
                ('actor', models.ForeignKey(to='services.Actor')),
                ('movie', models.ForeignKey(to='services.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='PostRelatedNotif',
            fields=[
                ('notification_ptr', models.OneToOneField(auto_created=True, primary_key=True, to='services.Notification', serialize=False, parent_link=True)),
                ('post', models.ForeignKey(to='services.Post')),
            ],
            bases=('services.notification',),
        ),
        migrations.AddField(
            model_name='notification',
            name='notif_object',
            field=models.ForeignKey(to='users.Member', related_name='object'),
        ),
        migrations.AddField(
            model_name='notification',
            name='notif_subject',
            field=models.ForeignKey(to='users.Member', related_name='subject'),
        ),
        migrations.AddField(
            model_name='like',
            name='post',
            field=models.ForeignKey(to='services.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, to='services.Post'),
        ),
    ]
