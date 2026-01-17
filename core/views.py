from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import UserProfile, Chat
from .forms import UserProfileForm, LoginForm, UserProfileUpdateForm, NewChatForm

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
    
# class NewChatView(View):
#     model = Chat
#     form_class = NewChatForm
#     template_name = 'core/new_chat.html'
#     success_url = reverse_lazy('core:profile_detail')

#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})
    
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             chat = form.save(commit=False)
#             chat.save()
#             chat.participants.add(request.user.user_profile)
#             form.save()
#             messages.success(request, "Новий чат успішно створено!")
#             return redirect(self.success_url)
#         return render(request, self.template_name, {'form': form})

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