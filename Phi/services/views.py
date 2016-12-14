import datetime
import operator

from math import floor
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

from . import models
from users.models import Member
from .forms import SendPostModelForm, EditProfileForm
from users.forms import MemberRegModelForm, MemberLoginForm

class TemplatePost():

	def __init__(self, post, member):
		self.post = post
		self.rate = floor(post.rate)
		self.crate = 10 - self.rate
		self.like_num = len(list(models.Like.objects.filter(post=post)))
		if len(models.Like.objects.filter(member=member, post=post)) > 0:
			self.liked = True
		else:
			self.liked = False
		self.comment_num = len(list(models.Comment.objects.filter(post=post)))
		self.comments = list(models.Comment.objects.filter(post=post).order_by('datetime'))

def home(request):
	if request.user.is_authenticated():
		member = Member.objects.get(user=request.user)
		followees = member.followees.all()
		
		posts = []
		for followee in followees:
			posts += models.Post.objects.filter(member=followee)

		posts = sorted(posts, key=operator.attrgetter('datetime'), reverse=True)

		template_posts = []
		for post in posts:
			template_posts += [TemplatePost(post, member)]

		layout = get_layout(member)

		return render(request, 'view-timeline.html', {
				'template_posts': template_posts,
				'member': member,
				'like_notifs': layout['like_notifs'],
				'comment_notifs': layout['comment_notifs'],
				'follow_notifs': layout['follow_notifs'],
				'mozakhraf_notifs': layout['mozakhraf_notifs'],
				'notif_num': layout['notif_num'],
				'recmovies': layout['recmovies'],
				'recusers': layout['recusers']
			})
	else:
		login_form = MemberLoginForm()
		reg_form = MemberRegModelForm()
		return render(request, 'new-visit.html', {
				'login_form': login_form,
				'reg_form': reg_form
			})

def answer(request):
	return render(request, 'FAQ.html')

def get_user_profile(request, username):
	if request.user.is_authenticated():
		# khodesh
		member = Member.objects.get(user=request.user)

		# uni ke mikhad bebine
		member_to_visit = Member.objects.filter(user__username=username)[0]

		my_if_get(request)

		if len(list(member.followees.filter(user__username=username))) == 0: # he is not following!
			do_i_follow_her = False
		else:
			do_i_follow_her = True

		if member_to_visit == member:
			this_is_me = True
		else:
			this_is_me = False
		
		# post haaye member_to_visit
		posts = list(models.Post.objects.filter(member=member_to_visit).order_by('-datetime'))

		template_posts = []
		for post in posts:
			template_posts += [TemplatePost(post, member)]

		num_of_followers = len(member_to_visit.member_set.all())
		num_of_followees = len(member_to_visit.followees.all())

		layout = get_layout(member)		

		return render(request, 'view-user-profile.html', {
				'template_posts': template_posts[:20],
				'member_to_visit': member_to_visit,
				'num_of_followers': num_of_followers,
				'num_of_followees': num_of_followees,
				'this_is_me': this_is_me,
				'member': member,
				'like_notifs': layout['like_notifs'],
				'comment_notifs': layout['comment_notifs'],
				'follow_notifs': layout['follow_notifs'],
				'mozakhraf_notifs': layout['mozakhraf_notifs'],
				'notif_num': layout['notif_num'],
				'recmovies': layout['recmovies'],
				'recusers': layout['recusers'],
				'do_i_follow_her': do_i_follow_her
			})
	else:
		login_form = MemberLoginForm()
		reg_form = MemberRegModelForm()
		return render(request, 'new-visit.html', {
				'login_form': login_form,
				'reg_form': reg_form
			})


def my_if_get(request):
	if request.GET:
		notif_id = request.GET['notifID']
		notif = models.Notification.objects.get(id=notif_id)
		notif.seen = True
		notif.save()


def edit_user_profile(request, username):
	if request.user.is_authenticated():
		member = Member.objects.get(user=request.user)

		if request.method == 'POST':
			form = EditProfileForm(member, request.POST, request.FILES)
			if form.is_valid():
				first_name = form.cleaned_data['first_name']
				if first_name!='':
					member.user.first_name = first_name
				last_name = form.cleaned_data['last_name']
				if last_name!='':
					member.user.last_name = last_name
				displayed_name = form.cleaned_data['displayed_name']
				if displayed_name!='':
					member.displayed_name = displayed_name
				bio = form.cleaned_data['bio']
				if bio!='':
					member.bio = bio
				birthday = form.cleaned_data['birthday']
				if birthday is not None:
					member.birthday = birthday
				password = form.cleaned_data['password']
				if password!='':
					member.user.set_password(password)
					member.user.save() # in mohemeha! :))
					user = authenticate(username=member.user.username, password=password) # in mohemeha! :))
					login(request, user)
				if request.FILES:
					member.prof_image = request.FILES['prof_image']
				member.save()
				return HttpResponseRedirect('/members/' + member.user.username + '/')
			
			layout = get_layout(member)
			return my_render_method(form, layout, member, request)
		else:
			if member.user.username != username:
				return HttpResponseRedirect('/members/' + member.user.username + '/edit/')

			form = EditProfileForm(member=member)
			layout = get_layout(member)
			return my_render_method(form, layout, member, request)
	else:
		login_form = MemberLoginForm()
		reg_form = MemberRegModelForm()
		return render(request, 'new-visit.html', {
				'login_form': login_form,
				'reg_form': reg_form
			})


def my_render_method(form, layout, member, request):
	return render(request, 'edit-user-profile.html', {
		'form': form,
		'member': member,
		'like_notifs': layout['like_notifs'],
		'comment_notifs': layout['comment_notifs'],
		'follow_notifs': layout['follow_notifs'],
		'mozakhraf_notifs': layout['mozakhraf_notifs'],
		'notif_num': layout['notif_num'],
		'recmovies': layout['recmovies'],
		'recusers': layout['recusers']
	})



def follow_unfollow(request, username):
	if request.user.is_authenticated():
		member = Member.objects.get(user=request.user)
		member_to_follow = Member.objects.get(user__username=username)
		if len(list(member.followees.filter(user__username=username))) == 0:
			# so: member follows member_to_follow
			member.followees.add(member_to_follow)

			new_notif = models.Notification()
			new_notif.notif_subject = member
			new_notif.notif_object = member_to_follow
			new_notif.notif_type = 'follow'
			new_notif.save()

			return HttpResponse('follow', status=200)
		else:
			# so: member un-follows member_to_follow
			member.followees.remove(member_to_follow)
			models.Notification.objects.filter(notif_subject=member, notif_object=member_to_follow, notif_type='follow').delete()
			return HttpResponse('unfollow', status=200)
	else:
		login_form = MemberLoginForm()
		reg_form = MemberRegModelForm()
		return render(request, 'new-visit.html', {
				'login_form': login_form,
				'reg_form': reg_form
			})

def get_followees(request, username):
	if request.user.is_authenticated():
		member = Member.objects.get(user=request.user)
		following = Member.objects.filter(user__username=username)[0].followees.all()
		followers = Member.objects.filter(user__username=username)[0].member_set.all()

		layout = get_layout(member)

		return my_render_method_5(followers, following, layout, member, request,'view-following-list.html')
	else:
		login_form = MemberLoginForm()
		reg_form = MemberRegModelForm()
		return render(request, 'new-visit.html', {
				'login_form': login_form,
				'reg_form': reg_form
			})

def my_render_method_5(followers, following, layout, member, request,str):
	return render(request, str, test(followers,following,member,layout))

def test(followers, following, member,layout):
	return {
		'following': following,
		'followers': followers,
		'member': member,
		'like_notifs': layout['like_notifs'],
		'comment_notifs': layout['comment_notifs'],
		'follow_notifs': layout['follow_notifs'],
		'mozakhraf_notifs': layout['mozakhraf_notifs'],
		'notif_num': layout['notif_num'],
		'recmovies': layout['recmovies'],
		'recusers': layout['recusers']
	}


def get_followers(request, username):
	if request.user.is_authenticated():
		member = Member.objects.get(user=request.user)
		
		followers = Member.objects.filter(user__username=username)[0].member_set.all()
		following = Member.objects.filter(user__username=username)[0].followees.all()

		layout = get_layout(member)

		return my_render_method_5(followers, following, layout, member, request,'view-followers-list.html')
	else:
		login_form = MemberLoginForm()
		reg_form = MemberRegModelForm()
		return render(request, 'new-visit.html', {
				'login_form': login_form,
				'reg_form': reg_form
			})




def get_single_post(request, post_id):
	if request.user.is_authenticated():
		member = Member.objects.get(user=request.user)

		my_if_get(request)
		
		post = models.Post.objects.get(id=post_id)

		template_post = TemplatePost(post, member)

		layout = get_layout(member)

		return my_render_method_6(layout, member, request, template_post)
	else:
		login_form = MemberLoginForm()
		reg_form = MemberRegModelForm()
		return render(request, 'new-visit.html', {
				'login_form': login_form,
				'reg_form': reg_form
			})


def my_render_method_6(layout, member, request, template_post):
	return render(request, 'view-single-post.html', {
		'template_post': template_post,
		'member': member,
		'like_notifs': layout['like_notifs'],
		'comment_notifs': layout['comment_notifs'],
		'follow_notifs': layout['follow_notifs'],
		'mozakhraf_notifs': layout['mozakhraf_notifs'],
		'notif_num': layout['notif_num'],
		'recmovies': layout['recmovies'],
		'recusers': layout['recusers']
	})


def like_unlike(request, post_id):
	if request.user.is_authenticated():
		member = Member.objects.get(user=request.user)

		if len(models.Like.objects.filter(member=member, post__id=post_id))  == 0:
			like = models.Like()
			like.member = member
			like.post = models.Post.objects.get(id=post_id)
			like.save()

			like_notif = models.PostRelatedNotif()
			like_notif.notif_subject = member
			like_notif.notif_object = like.post.member
			like_notif.notif_type = 'like'
			like_notif.post = like.post
			like_notif.save()

			return HttpResponse('Liked', status=200)
		else:
			models.Like.objects.filter(member=member, post__id=post_id).delete()
			models.PostRelatedNotif.objects.filter(notif_subject=member, notif_type='like', post__id=post_id).delete()

			return HttpResponse('Unliked', status=200)
	else:
		login_form = MemberLoginForm()
		reg_form = MemberRegModelForm()
		return render(request, 'new-visit.html', {
				'login_form': login_form,
				'reg_form': reg_form
			})

def comment(request, post_id):
	if request.user.is_authenticated():
		member = Member.objects.get(user=request.user)
		if request.method == "GET":	
			comment_text = request.GET.get('comment_text')
			post_id = request.GET.get('post-id')

			if not (comment_text and post_id):
				return HttpResponse("Not enough information.", status=400)

			postcomment = models.Comment()
			postcomment.member = member
			postcomment.post = models.Post.objects.filter(id=post_id)[0]
			postcomment.comment_text = comment_text
			postcomment.datetime = datetime.datetime.now()		
			postcomment.save()

			new_notif = models.PostRelatedNotif()
			new_notif.notif_subject = postcomment.member
			post_author_id = postcomment.post.member.id
			new_notif.notif_object = Member.objects.filter(id=post_author_id)[0]
			new_notif.notif_type = 'comment'
			new_notif.post = models.Post.objects.get(id=post_id)
			new_notif.save()

			other_comments = models.Comment.objects.filter(post__id=post_id).exclude(member=member)
			for comment in other_comments:
				if comment.member != comment.post.member and len(models.PostRelatedNotif.objects.filter(notif_subject=member, notif_object=comment.member, post__id=post_id, seen=False)) == 0:
					comment_notif = models.PostRelatedNotif()
					comment_notif.notif_subject = member
					comment_notif.notif_object = comment.member
					comment_notif.notif_type = 'mozakhraf'
					comment_notif.post = comment.post
					comment_notif.save()

			return HttpResponse(postcomment.datetime, status=200)
	else:
		login_form = MemberLoginForm()
		reg_form = MemberRegModelForm()
		return render(request, 'new-visit.html', {
				'login_form': login_form,
				'reg_form': reg_form
			})

def get_movie_profile(request, movie_id):
	if request.user.is_authenticated():
		member = Member.objects.get(user=request.user)

		movie = models.Movie.objects.get(id=movie_id)
		form = SendPostModelForm()
		roles = []
		available_roles = models.Role.objects.filter(movie=movie)
		for role in available_roles:
			roles += [role]

		layout = get_layout(member)		

		return my_render_method_7(form, layout, member, movie, request, roles)
	else:
		login_form = MemberLoginForm()
		reg_form = MemberRegModelForm()
		return render(request, 'new-visit.html', {
				'login_form': login_form,
				'reg_form': reg_form
			})


def my_render_method_7(form, layout, member, movie, request, roles):
	return render(request, 'view-movie-profile.html', {
		'movie': movie,
		'roles': roles,
		'form': form,
		'member': member,
		'like_notifs': layout['like_notifs'],
		'comment_notifs': layout['comment_notifs'],
		'follow_notifs': layout['follow_notifs'],
		'mozakhraf_notifs': layout['mozakhraf_notifs'],
		'notif_num': layout['notif_num'],
		'recmovies': layout['recmovies'],
		'recusers': layout['recusers']
	})


def rate_post(request, movie_id):
	if request.user.is_authenticated():
		member = Member.objects.get(user=request.user)
		if request.method == 'POST':
			form = SendPostModelForm(request.POST)
			if form.is_valid():
				mov_test(movie_id, request)
				if form.cleaned_data['post_text'] != '':
					post = form.save(commit=False)
					rate = int(request.POST['rate'])
					post.rate = rate
					movie = models.Movie.objects.get(id=int(movie_id))
					post.datetime = datetime.datetime.now()
					post.member = member
					post.movie = movie
					post.save()
				return HttpResponseRedirect('/movies/' + movie_id + '/')
			return HttpResponseRedirect('/movies/' + movie_id + '/')
	else:
		login_form = MemberLoginForm()
		reg_form = MemberRegModelForm()
		return render(request, 'new-visit.html', {
				'login_form': login_form,
				'reg_form': reg_form
			})


def mov_test(movie_id, request):
	rate = int(request.POST['rate'])
	movie = models.Movie.objects.get(id=int(movie_id))
	movie.avg_rate = round((movie.avg_rate * movie.total_raters + rate) / (movie.total_raters + 1), 1)
	movie.total_raters = movie.total_raters + 1
	movie.save()


def search(request):
	if request.user.is_authenticated():
		member = Member.objects.get(user=request.user)

		layout = get_layout(member)

		if request.method == "GET":
			word = request.GET.get('word', None)

			if word:
				members = list(Member.objects.filter(user__username__icontains=word))
				movies = list(models.Movie.objects.filter(name__icontains=word))
			else:
				members = []
				movies = []

			return my_render_method_8(layout, member, members, movies, request, word)
		else:
			return HttpResponseRedirect('../')
	else:
		login_form = MemberLoginForm()
		reg_form = MemberRegModelForm()
		return render(request, 'new-visit.html', {
				'login_form': login_form,
				'reg_form': reg_form
			})


def my_render_method_8(layout, member, members, movies, request, word):
	return render(request, 'view-search-results.html', {
		'member': member,
		'like_notifs': layout['like_notifs'],
		'comment_notifs': layout['comment_notifs'],
		'follow_notifs': layout['follow_notifs'],
		'mozakhraf_notifs': layout['mozakhraf_notifs'],
		'notif_num': layout['notif_num'],
		'recmovies': layout['recmovies'],
		'recusers': layout['recusers'],
		'members': members,
		'movies': movies,
		'word': word
	})


def get_recmovies():
	recmovies = models.Movie.objects.order_by('?')[:3]
	return recmovies

def get_recusers(member):
	member_followees = member.followees.all()
	followees_id = []
	for followee in member_followees:
		followees_id += [followee.id]
	recusers = Member.objects.exclude(id__in=followees_id).order_by('?')[:3]
	return recusers

def get_layout(member):
	notifs = list(models.PostRelatedNotif.objects.filter(notif_object=member, seen=False))
	notifs += list(models.Notification.objects.filter(notif_object=member, notif_type='follow', seen=False))
	like_notifs = []
	comment_notifs =[]
	follow_notifs = []
	mozakhraf_notifs = []

	for notif in notifs:
		if notif.notif_type == 'like':
			like_notifs += [notif]
		elif notif.notif_type == 'comment':
			comment_notifs += [notif]
		elif notif.notif_type == 'follow':
			follow_notifs += [notif]
		elif notif.notif_type == 'mozakhraf':
			mozakhraf_notifs += [notif]

	recmovies = get_recmovies()
	recusers = get_recusers(member)

	return {'like_notifs':like_notifs,
			'comment_notifs':comment_notifs,
			'follow_notifs':follow_notifs,
			'mozakhraf_notifs':mozakhraf_notifs,
			'notif_num':len(notifs),
			'recmovies':recmovies,
			'recusers':recusers}
