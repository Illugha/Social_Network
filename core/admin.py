from django.contrib import admin
from .models import Chat, UserProfile, Message, Post

admin.site.register(UserProfile)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Post)
