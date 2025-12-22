from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserProfileForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'bio', 'avatar')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            
            # Створюємо/оновлюємо профіль завжди, без умов
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'bio': self.cleaned_data['bio'], 'role': 'member'}
            )
            if not created:  # якщо вже був - просто оновлюємо поля
                profile.bio = self.cleaned_data['bio'] or profile.bio
                if self.cleaned_data['avatar']:
                    profile.avatar = self.cleaned_data['avatar']
                profile.save()
            else:
                if self.cleaned_data['avatar']:
                    profile.avatar = self.cleaned_data['avatar']
                    profile.save()

        return user