from django.contrib import admin
from .models import BaiJie


class BaijieAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publish")
    search_fields = ("title", "body")
    raw_id_fields = ("author",)
    ordering = ['publish']


admin.site.register(BaiJie, BaijieAdmin)

# Register your models here.
