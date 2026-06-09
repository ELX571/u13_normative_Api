from django.contrib import admin

from posting.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass 