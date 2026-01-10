from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import UserProfile
from .forms import UserProfileForm, LoginForm

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
        return render(request, 'core/profile_detail.html', {'profile': profile})

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
    form_class = UserProfileForm
    template_name = 'core/profile_update.html'
    success_url = reverse_lazy('core:profile_detail')

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)