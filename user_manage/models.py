from django.db import models
from django.contrib.auth.models import AbstractUser,User

class User(AbstractUser):
    is_owner = models.BooleanField('owne status',default=False)
    is_client = models.BooleanField('client status',default=False)


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name='proprietario')

    def __str__(self):
        return self.user.username

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='cliente')


    def __str__(self):
        return self.user.username