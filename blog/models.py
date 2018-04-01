# -*- coding: utf-8 -*-

import markdown
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['-id']

    #def get_absolute_url(self):
    #    return reverse('blog:category', kwargs={'pk': self.pk})

    # 统计分类下的文章数量
    def get_blog_count(self):
        # Django数据库API：跨关联关系查询
        # 要跨越关联关系，只需使用关联的模型字段的名称，并使用双下划线分隔，直至你想要的字段
        return BlogArticles.objects.filter(category__name=self).count()

    def __str__(self):
        return self.name


class BlogArticles(models.Model):
    title = models.CharField(max_length=60)
    author = models.ForeignKey(User, related_name="blog_post")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    excerpt = models.CharField(max_length=200, blank=True)
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, related_name="cate_post", blank=True, null=True)

    class Meta:
        ordering = ("-publish",)

    def get_absolute_url(self):
        # reverse(viewname, args, kwargs)函数的调用方式：
        # viewname 就是每个应用的 url.py 中设置 URL 时 name 的值，书p135
        # 即 应用： URL名
        return reverse('blog:blog_detail', kwargs={'article_id': self.pk})

    # 阅读数
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 自动生成摘要
    def save(self, *args, **kwargs):
        # 如果没有写摘要
        if not self.excerpt:
            # 首先实例化一个Markdown类，用于渲染body的文本
            md = markdown.Markdown(extensions=[
                 'markdown.extensions.extra',
                 'markdown.extensions.codehilite',
            ])
        # 先将 Markdown 文本渲染成 html文本
        # strip_tags 去掉html文本的全部 html 标签
        # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:90]

        # 调用父类的save方法将数据保存到数据库中
        super(BlogArticles, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
