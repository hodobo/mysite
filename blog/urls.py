# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from . import views


urlpatterns = [
    # IndexView 是一个类，不能直接替代 index 函数。这里调用的是as_view（）方法，将一个类转换成一个函数
    url(r'^$', views.IndexView.as_view(), name="index"),

    # （?P<article_id>\d）的作用是从用户访问的URL里把匹配的字符串捕获并作为关键字参数传给对应的视图函数article_detail
    url(r'^article/(?P<article_id>\d+)/$', views.BlogDetailView.as_view(), name="blog_detail"),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^category/([\w\s]+)/$', views.CategoryDetail.as_view(), name='category'),
]
