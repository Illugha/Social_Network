from urllib import request
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View, UpdateView, DeleteView, FormView, ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.urls import reverse
from .models import UserProfile, Chat, Post, Message
from .forms import *

class UserCreationView(FormView):
    form_class = UserProfileForm
    template_name = 'core/profile_creation.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Профіль успішно створено! Ласкаво просимо!")
        return redirect('core:profile_detail')

class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'core/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id')
        return get_object_or_404(UserProfile, user__id=user_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = self.object.chats.all() if hasattr(self.object, 'chats') else []
        return context

class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'core/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, "Ви успішно увійшли!")
            return redirect('core:profile_detail', user_id=user.id)
        else:
            form.add_error(None, "Невірний логін або пароль")
            return self.form_invalid(form)

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('core:home_page')

class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileUpdateForm
    template_name = 'core/profile_update.html'

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)
    
    def get_success_url(self):
        return reverse('core:profile_detail', kwargs={'user_id': self.request.user.id})

class NewPostView(View):
    model = Post
    form_class = NewPostForm
    template_name = 'core/new_post.html'
    success_url = reverse_lazy('core:user_posts')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = self.object.chats.all() if hasattr(self.object, 'chats') else []
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.user_profile
            post.save()
            form.save_m2m()

            messages.success(request, "Новий пост успішно створено!")
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})

class logoutView(LogoutView):
    next_page = reverse_lazy('core:login')

class UserListView(ListView):
    model = User
    template_name = 'core/user_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['chats'] = self.request.user.user_profile.chats.all()
        else:
            context['chats'] = []
        return context

    def get_queryset(self):
        queryset = User.objects.all()

        q_username = self.request.GET.get('q_username')
        profile_id = self.request.GET.get('profile_id')

        if q_username:
            queryset = queryset.filter(username__icontains=q_username)

        if profile_id:
            queryset = queryset.filter(user_profile__id=profile_id)

        return queryset.order_by('username')

class UpdatePostView(UpdateView):
    model = Post
    form_class = NewPostForm
    template_name = 'core/update_post.html'

    def get_object(self, queryset=None):
        post_id = self.kwargs.get('post_id')
        return Post.objects.get(id=post_id, author=self.request.user.user_profile)

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse('core:user_posts', kwargs={'profile_id': self.object.author.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = self.request.user.user_profile.chats.all() if self.request.user.is_authenticated else []
        return context

class DeletePostView(DeleteView):
    model = Post
    template_name = 'core/delete_post.html'

    def get_object(self, queryset=None):
        post_id = self.kwargs.get('post_id')
        return Post.objects.get(id=post_id, author=self.request.user.user_profile)

    def get_success_url(self):
        return reverse('core:user_posts', kwargs={'profile_id': self.object.author.id})

class UserPostsView(ListView):
    model = Post
    template_name = 'core/user_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.profile = get_object_or_404(
            UserProfile,
            id=self.kwargs['profile_id']
        )
        return Post.objects.filter(
            author=self.profile
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        user_profile = getattr(self.request.user, 'user_profile', None)
        context['chats'] = user_profile.chats.all() if user_profile else []
        return context

class NewChatView(View):
    model = Chat
    form_class = NewChatForm
    template_name = 'core/new_chat.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.creator = request.user.user_profile
            chat.save()

            if chat.availability == 'private':
                participants = form.cleaned_data.get('participants')
                if participants:
                    chat.participants.set(participants)
                chat.participants.add(request.user.user_profile)
            else:
                chat.participants.add(request.user.user_profile)

            messages.success(request, "Chat has been created!")
            return redirect('core:chat_detail', chat_id=chat.id)
        else:
            print(form.errors)
            return render(request, self.template_name, {'form': form})

class ChatDetailView(View):
    def get(self, request, chat_id, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404()

        chat = get_object_or_404(Chat, id=chat_id)

        user_profile = request.user.user_profile

        if chat.availability == 'private' and user_profile not in chat.participants.all():
            raise Http404()

        return render(request, 'core/chat_detail.html', {
            'chat': chat,
            'messages': chat.messages.select_related('sender__user'),
        })

class ChatRenameView(UpdateView):
    form_class = ChatRenameForm
    template_name = 'core/rename_chat.html'

    def get_object(self, queryset=None):
        chat_id = self.kwargs.get('chat_id')
        participants = self.request.user.user_profile
        return get_object_or_404(Chat, id=chat_id, participants=participants, creator=self.request.user.user_profile)
    
    def get_success_url(self):
        return reverse('core:chat_detail', kwargs={'chat_id': self.object.id})

class ChatDeleteView(DeleteView):
    model = Chat
    template_name = 'core/delete_chat.html'

    def get_success_url(self):
        return reverse('core:profile_detail', kwargs={'user_id': self.request.user.id})

class HomePageView(ListView):
    model = Post
    template_name = 'core/home_page.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')[:10]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['chats'] = self.request.user.user_profile.chats.all()
        else:
            context['chats'] = []
        return context

class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm

    def form_valid(self, form):
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, id=chat_id)
        message = form.save(commit=False)
        message.chat = chat
        message.sender = self.request.user.user_profile
        message.save()
        return redirect('core:chat_detail', chat_id=chat.id)

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'core/delete_message.html'

    def get_success_url(self):
        return reverse('core:chat_detail', kwargs={'chat_id': self.object.chat.id})

class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'core/update_message.html'

    def get_success_url(self):
        return reverse('core:chat_detail', kwargs={'chat_id': self.object.chat.id})


class PublicChatsListView(ListView):
    model = Chat
    template_name = 'core/public_chats_list.html'
    context_object_name = 'public_chats'

    def get_queryset(self):
        return Chat.objects.filter(availability='public').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['chats'] = self.request.user.user_profile.chats.all()
        else:
            context['chats'] = []
        return context

class LikePostView(View):
    def post(self, request, post_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('core:login')

        post = get_object_or_404(Post, id=post_id)
        user_profile = request.user.user_profile

        if user_profile in post.likes.all():
            post.likes.remove(user_profile)
        else:
            post.likes.add(user_profile)

        return redirect('core:user_posts', profile_id=post.author.id)