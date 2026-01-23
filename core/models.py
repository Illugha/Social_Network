from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('moderator', 'Moderator'),
        ('member', 'Member'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    likes = models.ManyToManyField(UserProfile, related_name='liked_posts', blank=True)
    link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Chat(models.Model):
    AVAILABILITY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )

    name = models.CharField(max_length=255, default='New Chat')
    participants = models.ManyToManyField(UserProfile, related_name='chats')
    availability = models.CharField(max_length=50, choices=AVAILABILITY_CHOICES, default='private')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id} with {self.participants.count()} participants"
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.user.username} at {self.timestamp}"