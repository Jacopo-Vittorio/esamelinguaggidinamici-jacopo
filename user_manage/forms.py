from crispy_forms import helper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from user_manage.models import User, Owner, Cliente

from crispy_forms.helper import FormHelper



class ClienteSignUpForm(UserCreationForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    #queryset = Cliente.objects.all()
    class Meta(UserCreationForm.Meta):
        model = User


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        user.save()
        client = Cliente.objects.create(user=user)
        #client.queryset.add(*self.cleaned_data.get('dati'))
        return user


class OwnerSignUpForm(UserCreationForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    #queryset = Owner.objects.all()
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_owner = True
        user.save()
        owner = Owner.objects.create(user=user)
        #owner.queryset.add(*self.cleaned_data.get('dati'))
        return user