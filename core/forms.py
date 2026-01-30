from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Chat, Post, Message


class UserProfileForm(UserCreationForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Расскажите о себе…',
            'rows': 3
        }),
        required=False
    )
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Имя пользователя'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Электронная почта'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })


    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'bio': self.cleaned_data['bio'], 'role': 'member'}
            )
            if not created:
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
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))



class UserProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Расскажите о себе…',
            'rows': 3
        }),
        required=False
    )
    avatar = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('bio', 'avatar')

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile

class NewChatForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=UserProfile.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Chat
        fields = ('name', 'availability', 'participants')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Название чата'
        })
        self.fields['availability'].widget.attrs.update({
            'class': 'form-control'
        })


    def save(self, commit=True):
        chat = super().save(commit=False)

        if commit:
            chat.save()
            self.save_m2m()

        return chat
    
class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'video', 'link')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Заголовок поста'
        })
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Содержание поста',
            'rows': 5
        })

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'video', 'link')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Заголовок поста'
        })
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Содержание поста',
            'rows': 5
        })

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите сообщение...',
            'rows': 3
        })