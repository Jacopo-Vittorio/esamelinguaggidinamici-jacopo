from django.contrib.auth import login
from django.contrib.auth.models import AbstractUser
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import CreateView
from user_manage.forms import OwnerSignUpForm, ClienteSignUpForm
from user_manage.models import User


class ClienteSignUpView(CreateView):
    model = User
    form_class = ClienteSignUpForm
    template_name = 'user_manage/registration/user_creation.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'cliente'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return redirect('homepage')

class OwnerSignUpView(CreateView):
    model = User
    form_class = OwnerSignUpForm
    template_name = 'user_manage/registration/owner_creation.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'owne'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return redirect('homepage')





