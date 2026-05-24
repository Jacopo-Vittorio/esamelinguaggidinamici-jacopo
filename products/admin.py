from django.contrib import admin
from products.models import  Prodotti, Categoria,Review
# Register your models here.
admin.site.register(Prodotti)
admin.site.register(Categoria)
admin.site.register(Review)