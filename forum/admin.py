from django.contrib import admin

# Register your models here.
from forum.models import Forum, Risposta

admin.site.register(Forum)
admin.site.register(Risposta)