
from django.db import models

from users.models import Member

class Movie(models.Model):
	name = models.CharField(max_length=100)
	year = models.PositiveSmallIntegerField()
	avg_rate = models.FloatField()
	link_to_imdb = models.CharField(max_length=300)
	total_raters = models.PositiveIntegerField()
	summary = models.TextField()
	genre = models.CharField(max_length=40)
	initial_release = models.DateField()
	director = models.CharField(max_length=100)
	country = models.CharField(max_length=40)
	author = models.CharField(max_length=100)
	song_writer = models.CharField(max_length=100)
	cinematography = models.CharField(max_length=100)
	running_time = models.PositiveSmallIntegerField()
	poster_image = models.ImageField(upload_to='media/', blank="True", null=True, default='media/unknown-movie.png')

	def __str__(self):
		return self.name

class Actor(models.Model):
	name = models.CharField(max_length=100)
	actor_image = models.ImageField(upload_to='media/', blank="True", null=True)

	def __str__(self):
		return self.name


class Role(models.Model):
	actor = models.ForeignKey(Actor)
	movie = models.ForeignKey(Movie)
	role_name = models.CharField(max_length=50)

	def __str__(self):
		return self.role_name

class Post(models.Model):
 	member = models.ForeignKey(Member, related_name="author")
 	movie = models.ForeignKey(Movie)
 	rate = models.PositiveSmallIntegerField()
 	post_text = models.TextField(max_length=500)
 	datetime = models.DateTimeField()

 	def __str__(self):
 		return self.post_text[:30]

class Like(models.Model):
	member = models.ForeignKey(Member)
	post = models.ForeignKey(Post)

class Comment(models.Model):
	member = models.ForeignKey(Member)
	post = models.ForeignKey(Post, null=True)
	comment_text = models.TextField()
	datetime = models.DateTimeField()

	def __str__(self):
		return self.comment_text[:30]

class Notification(models.Model):
	notif_subject = models.ForeignKey(Member, related_name="subject")
	notif_object = models.ForeignKey(Member, related_name="object")
	notif_type = models.CharField(max_length=20)
	seen = models.BooleanField(default=False)

class PostRelatedNotif(Notification):
	post = models.ForeignKey(Post)
