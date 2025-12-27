from django.urls import path
from .views import *

app_name = 'core'
urlpatterns = [
    path('create_profile/', UserCreationView.as_view(), name='create_profile'),
    path('profile_detail//<int:pk>/', UserProfileDetailView.as_view(), name='profile_detail'),
    path('login/', LoginFormView.as_view(), name='login'),
]