from django.contrib import admin

# Register your models here.
from checkout.models import Order, OrderItem

admin.site.register(OrderItem)
admin.site.register(Order)
