import captcha.urls

from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from services import views as services_views
from users import views as users_views


urlpatterns = [
    url(r'^$', services_views.home),
    url(r'^FAQ/$', services_views.answer),
    url(r'^login/$', users_views.our_login),
    url(r'^register/$', users_views.register),
    url(r'^members/(?P<username>[\w|\d|_|@|+|.|-]+)/', include([
        url(r'^$', services_views.get_user_profile),
        url(r'^edit/$', services_views.edit_user_profile),
        url(r'^follow_unfollow/$', services_views.follow_unfollow),
        url(r'^following/$', services_views.get_followees),
        url(r'^followers/$', services_views.get_followers),
    ])),
    url(r'^posts/(?P<post_id>[\d]+)/', include([
            url(r'^$', services_views.get_single_post),
            url(r'^like_unlike/$', services_views.like_unlike),
            url(r'^comment/$', services_views.comment),
    ])),
    url(r'^movies/(?P<movie_id>[\d]+)/', include([
        url(r'^$', services_views.get_movie_profile),
        url(r'^rate_post/$', services_views.rate_post),
    ])),
    url(r'^search/$', services_views.search),
    url(r'^logout/$', users_views.our_logout),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include(captcha.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)