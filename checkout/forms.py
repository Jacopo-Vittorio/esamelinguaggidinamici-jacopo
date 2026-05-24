from crispy_forms.helper import FormHelper
from django import forms
from django.forms import CharField

from .models import Order

class OrderCreateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'

    class Meta:
        model= Order
        fields = ['firs_name','last_name','email','address','postal_code','city']

