# -*- coding: utf-8 -*-

from django.contrib import admin
from.models import BlogArticles, Category


# 为了让后台列出的信息更丰富点，才额外添加这些代码的
class BlogArticlesAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "publish")
#    list_filter = ("publish", "author")
    search_fields = ("title", "body")
    raw_id_fields = ("author",)
    date_hierarchy = "publish"  # ???????
    ordering = ['publish']


admin.site.register(Category)
admin.site.register(BlogArticles, BlogArticlesAdmin)

# Register your models here.
