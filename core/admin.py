from django.contrib import admin
from .models import Chat, UserProfile

admin.site.register(UserProfile)
admin.site.register(Chat)
