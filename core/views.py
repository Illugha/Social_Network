from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import UserProfile
from .forms import UserProfileForm

class UserCreationView(CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'core/profile_creation.html'
    success_url = reverse_lazy('profile_detail')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Профіль успішно створено! Ласкаво просимо!")
        return redirect('core:profile_detail')

class UserProfileDetailView(View):
    def get(self, request, *args, **kwargs):
        profile = UserProfile.objects.get(user=request.user)
        return render(request, 'core/profile_detail.html', {'profile': profile})