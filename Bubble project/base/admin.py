from django.contrib import admin
from .models import Post, UserProfile,ChatRoom


admin.site.register(Post)

admin.site.register(UserProfile)
admin.site.register(ChatRoom)
