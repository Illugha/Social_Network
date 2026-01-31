from django.urls import path
from .views import *

app_name = 'core'
urlpatterns = [
    path('create_profile/', UserCreationView.as_view(), name='create_profile'),
    path('profile_detail/<int:user_id>/', UserProfileDetailView.as_view(), name='profile_detail'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('profile_update/', UserProfileUpdateView.as_view(), name='profile_update'),
    path('new_chat/', NewChatView.as_view(), name='new_chat'),
    path('chat/<int:chat_id>/', ChatDetailView.as_view(), name='chat_detail'),
    path('chat/<int:pk>/delete/', ChatDeleteView.as_view(), name='delete_chat'),
    path('chat/<int:chat_id>/send/', MessageCreateView.as_view(), name='new_message'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='delete_message'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='update_message'),
    path('', HomePageView.as_view(), name='home_page'),
    path('new_post/', NewPostView.as_view(), name='new_post'),
    path('update_post/<int:post_id>/', UpdatePostView.as_view(), name='update_post'),
    path('delete_post/<int:post_id>/', DeletePostView.as_view(), name='delete_post'),
    path('profile/<int:profile_id>/posts/',UserPostsView.as_view(),name='user_posts'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('logout/', LogoutView.as_view(next_page='core:login'), name='logout'),
    path('public_chat_list/', PublicChatsListView.as_view(), name='public_chat_list'),
    path('like_post/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('chat/<int:chat_id>/rename/', ChatRenameView.as_view(), name='chat_rename'),
    path('chat/<int:chat_id>/leave/', LeaveChatView.as_view(), name='leave_chat'),
    ]