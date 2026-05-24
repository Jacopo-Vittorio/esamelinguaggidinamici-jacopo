
from django.urls import path
from django.contrib.auth import views as auth_views

from user_manage import views

app_name = 'utente'

urlpatterns =[
path('registration/client', views.ClienteSignUpView.as_view(), name='user-create'),
path('registration/owne', views.OwnerSignUpView.as_view(), name='owne-create')
]