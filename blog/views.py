# -*- coding: utf-8 -*-

import markdown
from django.shortcuts import get_object_or_404
from .models import BlogArticles, Category
from django.views.generic import ListView, DetailView, TemplateView


class AboutView(TemplateView):
    template_name = "blog/about.html"


class Lianxi(TemplateView):
    template_name = "blog/contact.html"


class IndexView(ListView):
    model = BlogArticles
    template_name = 'blog/index.html'
    context_object_name = 'blogs'

    # 类视图 ListView 已经帮我们写好了分页逻辑，我们只需通过指定 paginate_by属性来开启分页功能即可
    # 指定 paginate_by 属性即可开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 3

    # 重写此方法，因为博客的‘分类’与‘blogs’共用了blog/index.html模板，
    # 所以需上下文传多一个Category的值‘category_list’给模板
    # 通过覆盖该方法返回额外的上下文
    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        ctx['category_list'] = Category.objects.all()
        return ctx


class BlogDetailView(DetailView):
    model = BlogArticles
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'
    # pk_url_kwarg用于接收一个来自url中的主键，然后会根据这个主键进行查询

    def get(self, request, *args, **kwargs):
        # 复写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 BlogArticles 模型实例，即被访问的文章 article
        response = super(BlogDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 article
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    # get_object 方法默认情况下获取 id 为pk_url_kwarg 的对象,如果需要在获取过程中对获取的对象做一些处理,
    # 比如对文章做 markdown 拓展，通过复 写 get_object 即可实现
    def get_object(self, queryset=None):
        # （复写 get_object 方法以增加获取单个 model 对象的其他逻辑）
        # 复写 get_object 方法的目的是因为需要对 article 的 body 值进行渲染
        obj = super(BlogDetailView, self).get_object(queryset=None)
        obj.body = markdown.markdown(obj.body,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ])
        return obj

    def get_context_data(self, **kwargs):
        ctx = super(BlogDetailView, self).get_context_data(**kwargs)
        ctx['category_list'] = Category.objects.all()
        return ctx

"""
def article_detail(request, article_id):
    #article = BlogArticles.objects.get(id=article_id)

    article = get_object_or_404(BlogArticles, id=article_id)
    article.increase_views()

    article.body = markdown.markdown(article.body,
                                     extensions=[
                                        'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ])
    pub = article.publish
    return render(request, "blog/detail.html", {"article": article})


def category(request, pk):
    # cate = get_object_or_404(Category, pk=pk)
    blogs = BlogArticles.objects.filter(category=pk).order_by('-publish')
    # blogs = cate.cate_post.all()
    return render(request, 'blog/index.html', context={'blogs': blogs})

"""


class CategoryDetail(IndexView):
    #context_object_name = "blogs"
    #template_name = 'blog/index.html'
    #paginate_by = 3

    # 参照了Django文档：“基于类的内建通用视图”之动态过滤.
    # https://yiyibooks.cn/xx/django_182/topics/class-based-views/generic-display.html
    # 重写get_queryset()方法，
    # 类视图被调用时，各种有用的对象被存储在self上
    # 其中包含了从URLconf中获取到的位置参数 (self.args)和基于名字的参数(self.kwargs)(关键字参数)。
    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.args[0])
        blogs = BlogArticles.objects.filter(category=self.category)
        return blogs

    #def get_queryset(self):
    #    cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
    #    return super(CategoryDetail, self).get_queryset().filter(category=cate)

    #def get_context_data(self, **kwargs):
    #    ctx = super(CategoryDetail, self).get_context_data(**kwargs)
    #    ctx['category_list'] = Category.objects.all()
    #    return ctx
