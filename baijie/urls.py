# -*- coding: utf-8 -*-
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name="home"),
    url(r'(?P<article_id>\d+)/$', views.BaijieDetailView.as_view(), name="blog_detail"),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^movie/$', views.movieview, name='movie'),
    url(r'^about/$', views.aboutview, name='about'),
]