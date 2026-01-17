from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Chat


class UserProfileForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email')

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
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('bio', 'avatar')

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile

# class NewChatForm(forms.ModelForm):
#     name = forms.CharField(max_length=255, initial='New Chat')

#     availability = forms.ChoiceField(choices=[
#         ('public', 'Public'),
#         ('private', 'Private'),
#     ])
#     participants = forms.ModelMultipleChoiceField(
#         queryset=UserProfile.objects.all(),
#         widget=forms.CheckboxSelectMultiple
#     )

#     class Meta:
#         model = Chat
#         fields = ('name', 'availability', 'participants')

#     def save(self, commit=True):
#         chat = Chat(
#             availability=self.cleaned_data['availability'],
#             name = self.cleaned_data['name']
#         )
#         if commit:
#             chat.save()
#             chat.participants.set(self.cleaned_data['participants'])
#         return chat

class NewChatForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=UserProfile.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Chat
        fields = ('name', 'availability', 'participants')

    def save(self, commit=True):
        chat = super().save(commit=False)

        if commit:
            chat.save()
            self.save_m2m()

        return chat