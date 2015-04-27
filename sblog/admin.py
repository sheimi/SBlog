from django.contrib import admin

from sblog.models import Post, Tag, Category


# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
