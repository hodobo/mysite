# -*- coding: utf-8 -*-

import markdown
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.html import strip_tags


class BaiJie(models.Model):
    title = models.CharField(max_length=60)
    author = models.ForeignKey(User, related_name='blog_baijie')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    excerpt = models.CharField(max_length=125, blank=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-publish",)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=['markdown.extensions.extra', ])
            self.excerpt = strip_tags(md.convert(self.body))[:90]
        super(BaiJie, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


# Create your models here.
