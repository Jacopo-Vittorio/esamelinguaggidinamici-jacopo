import datetime
import os
import random
from time import timezone

from django.db import models
from user_manage.models import User,Owner,Cliente
# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    # print(instance)
    #print(filename)
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext (filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
            )



class Categoria(models.Model):
    nome = models.CharField(max_length=255, null=False,blank=False)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return self.nome


class Prodotti(models.Model):
    owner = models.ForeignKey(Owner, related_name='prodotti', on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    #la related name la uso qui per fare subito delle operazioni sul DB
    name = models.CharField(max_length=255,)
    dimensione = models.CharField(max_length=255, default=None)
    tipo_materiale = models.CharField(max_length=255,default=None)
    price = models.CharField(max_length=255)

    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    #c'è la possibilità di andare a sovrascrivere alcune funzioni in base.py
    def __str__(self):
        return f'{self.name}'

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class Review(models.Model):
    prodotto = models.ForeignKey(Prodotti,related_name="recensioni", on_delete=models.CASCADE)
    user = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    comment_name = models.CharField(max_length=200)
    comment_body = models.TextField()
    rating_fornitore = models.IntegerField(choices=RATING,default=1)
    rating_prodotto = models.IntegerField(choices=RATING,default=1)
    def __str__(self):
        return f'{self.comment_name}'

class Report(models.Model):
    author = models.CharField(max_length=200)
    text = models.TextField()



    def __str__(self):
        return self.text

