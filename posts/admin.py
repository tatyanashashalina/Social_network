from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['owner', 'title', 'creation_date', 'hidden']


admin.site.register(Post, PostAdmin)
