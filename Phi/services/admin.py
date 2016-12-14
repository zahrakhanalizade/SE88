from django.contrib import admin

from .models import Movie, Actor, Role, Post, Like, Comment, Notification, PostRelatedNotif

class PostAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		obj.save()
		obj.movie.avg_rate = round((obj.movie.avg_rate * obj.movie.total_raters + obj.rate) / (obj.movie.total_raters + 1), 1)
		obj.movie.total_raters = obj.movie.total_raters + 1
		obj.movie.save()
		obj.save()

# Register your models here.
admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Role)
admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(PostRelatedNotif)