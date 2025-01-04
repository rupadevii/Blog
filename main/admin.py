from django.contrib import admin
from .models import Post, Comment, Notification, PrivateMessage, Category, Tag, UserProfile

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(PrivateMessage)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(UserProfile)

