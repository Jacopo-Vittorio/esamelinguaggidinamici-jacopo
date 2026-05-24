from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.views.generic.list import ListView
from cart.models import Cart
from checkout.forms import OrderCreateForm
from checkout.models import OrderItem
from user_manage.decorator import owner_required

class OrderCreateView(CreateView):
    form_class = OrderCreateForm
    initial = {'key':'value'}
    template_name = 'checkout/create.html'



    def post(self, request, *args, **kwargs):
        cart=Cart(request)
        form= self.form_class(request.POST)
        if form.is_valid():
            order=form.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],
                                         price=item['price'],quantity=item['quantity'])
            cart.clear()
            return render(request, 'checkout/completato.html', {'order': order})

        return render(request, self.template_name, {'cart': cart, 'form': form})



@method_decorator([login_required,owner_required],name='dispatch')
class ListaRichieste(ListView):
    model = OrderItem
    template_name = "checkout/gestione_ordini.html"
    context_object_name = 'ordini_list'

    def get_queryset(self):
        user = self.request.user

        qs = self.model.objects.filter(product__owner__user=user).order_by('order__created')

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListaRichieste, self).get_context_data(**kwargs)

        return context

class DetailOrder(DetailView):
    model = OrderItem
    template_name ="checkout/detail_ordine.html"

    def get_object(self, queryset=None):
        return get_object_or_404(OrderItem, pk=self.kwargs.get('pk'))

class DeleteOrder(DeleteView):
    model = OrderItem
    template_name ="checkout/delete_prod_order.html"
    success_url = reverse_lazy('homepage')

