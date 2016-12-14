import pydenticon

from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .models import Member
from .forms import MemberRegModelForm, MemberLoginForm

def our_login(request):
	if request.method == 'POST':
		form = MemberLoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['registered-username']
			password = form.cleaned_data['registered-password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect('/')
			return render(request, 'login.html', {'form': form, 'bad_login': True})
		return render(request, 'login.html', {'form': form, 'bad_login': True})
	else:
		form = MemberLoginForm()
		return render(request, 'login.html', {'form': form})

def register(request):
	if request.method == 'POST':
		form = MemberRegModelForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			password2 = form.cleaned_data['password2']
			email = form.cleaned_data['email']
			member = form.save(commit=False)
			user = User.objects.create_user(username=username, email=email, password=password)
			member.user = user
			human = True
			
			foreground = [
				"rgb(45,79,255)",
               	"rgb(254,180,44)",
               	"rgb(226,121,234)",
               	"rgb(30,179,253)",
               	"rgb(232,77,65)",
               	"rgb(49,203,115)",
               	"rgb(141,69,170)" ]
			background = "rgb(231,231,231)"
			identicon_generator = pydenticon.Generator(5, 5, foreground=foreground, background=background)
			identicon = identicon_generator.generate(username, 240, 240)
			f = open("media/media/" + username + ".png", "wb")
			f.write(identicon)
			f.close()
			member.prof_image = "media/" + username + ".png"
			
			member.save()
			return HttpResponseRedirect('/login/')
		return render(request, 'register.html', {'form': form})
	else:
		form = MemberRegModelForm()
		return render(request, 'register.html', {'form': form})

def our_logout(request):
	logout(request)
	return HttpResponseRedirect('/')
