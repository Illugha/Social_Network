from urllib import request
from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import UserProfile, Chat, Post
from .forms import *

class UserCreationView(FormView):
    form_class = UserProfileForm
    template_name = 'core/profile_creation.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Профіль успішно створено! Ласкаво просимо!")
        return redirect('core:profile_detail')

class UserProfileDetailView(View):
    def get(self, request, *args, **kwargs):
        profile = UserProfile.objects.get(user=request.user)
        chats = profile.chats.all()
        return render(request, 'core/profile_detail.html', {'profile': profile, 'chats': chats})

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
            return redirect('core:profile_detail')
        else:
            form.add_error(None, "Невірний логін або пароль")
            return self.form_invalid(form)

class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileUpdateForm
    template_name = 'core/profile_update.html'
    success_url = reverse_lazy('core:profile_detail')

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)

class NewPostView(View):
    model = Post
    form_class = NewPostForm
    template_name = 'core/new_post.html'
    success_url = reverse_lazy('core:user_posts')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

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

from django.urls import reverse

class DeletePostView(DeleteView):
    model = Post
    template_name = 'core/delete_post.html'

    def get_object(self, queryset=None):
        post_id = self.kwargs.get('post_id')
        return Post.objects.get(id=post_id, author=self.request.user.user_profile)

    def get_success_url(self):
        # после удаления редирект на страницу всех постов автора
        return reverse('core:user_posts', kwargs={'profile_id': self.object.author.id})

from django.views.generic import ListView
from django.shortcuts import get_object_or_404

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
        return context

class NewChatView(View):
    model = Chat
    form_class = NewChatForm
    template_name = 'core/new_chat.html'
    success_url = reverse_lazy('core:profile_detail')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.save()

            chat.participants.add(request.user.user_profile)
            form.save_m2m()

            messages.success(request, "Новий чат успішно створено!")
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})

class ChatDetailView(View):
    def get(self, request, chat_id, *args, **kwargs):
        chat = Chat.objects.get(id=chat_id)
        return render(request, 'core/chat_detail.html', {'chat': chat})

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/home_page.html')