from django.urls import path
from .views import UserCreationView

app_name = 'core'
urlpatterns = [
    path('create-profile/', UserCreationView.as_view(), name='create_profile'),
]