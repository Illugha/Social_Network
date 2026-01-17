from django.urls import path
from .views import *

app_name = 'core'
urlpatterns = [
    path('', UserCreationView.as_view(), name='create_profile'),
    path('profile_detail/', UserProfileDetailView.as_view(), name='profile_detail'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('profile_update/', UserProfileUpdateView.as_view(), name='profile_update'),
    path('new_chat/', NewChatView.as_view(), name='new_chat'),
    path('chat/<int:chat_id>/', ChatDetailView.as_view(), name='chat_detail'),
]