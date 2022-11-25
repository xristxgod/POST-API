from django.contrib import admin

from .models import User, Post, Comment, Image, Video


class UserAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    raw_id_fields = ('user',)
    list_display = ('title', 'text', 'active', 'user', 'created')


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    raw_id_fields = ('user', 'reply_comment')
    list_display = (
        'text', 'text', 'user', 'reply_comment',
        'content_type', 'object_id', 'content_object',

        'created'
    )


admin.site.register(Comment, CommentAdmin)
