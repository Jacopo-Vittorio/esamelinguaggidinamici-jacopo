from django.db import models

# Create your models here.
from user_manage.models import Owner, Cliente,User


class Forum(models.Model):
    fornitore = models.ForeignKey(Owner,on_delete=models.CASCADE)
    user = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    titolo =  models.CharField(max_length=255,)
    descrizione = models.CharField(max_length=255,)
    contenuto =  models.TextField()

    def __str__(self):
        return f'{self.titolo}'
class Risposta(models.Model):
    titolo = models.ForeignKey(Forum , related_name='risposta', on_delete=models.CASCADE)
    user = models.CharField(max_length=200)
    commento =models.TextField()

    def __str__(self):
        return  f'{self.commento}'
