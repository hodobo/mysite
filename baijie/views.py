# -*- coding: utf-8 -*-

import markdown
from .models import BaiJie
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView


# 使用django 自带的装饰器函数，参数login_url= 将没有登录的用户转到自定义的登录界面
@login_required(login_url='/baijie/login/')
def movieview(request):
    return render(request, 'baijie/movie.html')


def aboutview(request):
    return render(request, 'baijie/about.html')


class HomeView(ListView):
    model = BaiJie
    template_name = 'baijie/home.html'
    context_object_name = 'baijies'
    paginate_by = 3


class BaijieDetailView(DetailView):
    model = BaiJie
    template_name = 'baijie/detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'

    def get(self, request, *args, **kwargs):
        response = super(BaijieDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        obj = super(BaijieDetailView, self).get_object(queryset=None)
        # 有些扩展需要手动打开
        obj.body = markdown.markdown(obj.body, extensions=['markdown.extensions.extra', ])
        return obj
