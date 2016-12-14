
from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
	user = models.OneToOneField(User)
	displayed_name = models.CharField(max_length=255)
	bio = models.TextField(null=True)
	birthday = models.DateField()
	followees = models.ManyToManyField('Member', null=True) # kasani ke follow mikone
	prof_image = models.ImageField(upload_to='media/', blank="True")

	def __str__(self):
		return self.displayed_name + " (" + self.user.username + ")"