from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import View

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('blog:post_list')  # Redirect to homepage

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('blog:post_list')