from random import random

import comments as comments
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View

from cart.forms import CartAddProductForm
from user_manage.decorator import owner_required,client_required
from user_manage.views import OwnerSignUpView
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from products.models import Prodotti, Categoria, Review
from products.forms import ProdottiForm, ReviewForm, SearchForm, ReportForm, Lista_fornitoreForm, Lista_RevForm
from user_manage.models import Owner, Cliente
from django.conf import settings

def CategoriaView(request):
    category = request.GET.get('category')

    products = Prodotti.objects.filter(categoria__nome=category)

    categories = Categoria.objects.all()

    context = {
        'products': products,
        'categories': categories
    }

    return render(request, 'products/categoria.html', context)

class ProdottiList(ListView):
    model = Prodotti
    template_name = 'products/list.html'


# class ProdottiDetail(DetailView):
#     model = Prodotti
#     template_name = 'products/products_detail.html'
def product_related(request, pk):
        product = Prodotti.objects.get(id=pk)
        cart_product_form = CartAddProductForm()
        related_products = Prodotti.objects.filter(categoria=product.categoria).exclude(id=product.id)
        print(related_products)
        if len(related_products) >= 3:
            related_products = random.sample(related_products, 3)

        return render(request, 'products/products_detail.html',{'product':product,'related':related_products, 'cart_product_form': cart_product_form})

@method_decorator([login_required, owner_required], name='dispatch')
class ProdottiCreate(CreateView):
    model = Prodotti
    template_name = 'products/create.html'
    #fields = ['owne','name', 'description', 'price']
    success_url = reverse_lazy('homepage')
    form_class = ProdottiForm

    def form_valid(self, form):

        form.instance.owner = Owner.objects.get(user_id=self.request.user.id)
        return super(ProdottiCreate,self).form_valid(form)

@method_decorator([login_required, owner_required], name='dispatch')
class ProdottiDelete(DeleteView):
    model= Prodotti
    template_name = 'products/delete.html'
    success_url = reverse_lazy('homepage')
    success_message = 'Prodotto eliminato correttamente!'


@method_decorator([login_required, owner_required], name='dispatch')
class ProdottiUpdate(UpdateView):
    model = Prodotti
    template_name = 'products/update.html'
    #fields = ['owne','name','description','price']
    success_url = reverse_lazy('prod:products-category')
    form_class = ProdottiForm
    success_message = 'Prodotto modificato correttamente!'


@method_decorator([login_required,client_required],name='dispatch')
class RevDelete(DeleteView):
    model= Review
    template_name = 'products/delete_review.html'
    success_url = reverse_lazy('homepage')



@login_required()
def add_review(request, pk):
        object = Prodotti.objects.get(id=pk)
        if request.method == "POST":

            form = ReviewForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = Cliente.objects.get(user__username=request.user.username)
                comment.prodotto  = object
                comment.save()
                return redirect('prod:products-detail', pk=object.pk)
        else:
            form = ReviewForm()
        return render(request, 'products/recensioni.html', {'form': form})

@method_decorator([login_required, owner_required], name='dispatch')
class ReportView(CreateView):
    form_class = ReportForm
    initial = {'key':'value'}
    template_name = 'products/report_newcat.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.save()
            send_mail("Hello", "Prova", "salvatorebiancofanta@gmail.com", ["salvatorebianco15@gmail.com", ],
                      fail_silently=False)
            return redirect('homepage')

        return render(request, self.template_name, {'form': form})





class SearchView(ListView):
    model = Prodotti
    form_class = SearchForm
    template_name = "products/search2.html"
    context_object_name = 'search_list'
    success_url = reverse_lazy('prod:products-category')
    def get_queryset(self):


            nome= self.request.GET.get('nome')
            material=self.request.GET.get('material')
            min_price = self.request.GET.get('min_price')
            max_price = self.request.GET.get('max_price')
            if nome and material:
                                if min_price:
                                                if max_price:
                                                            qs = self.model.objects.filter(name__icontains=nome,tipo_materiale__icontains=material,price__gte=min_price,price__lte=max_price).order_by('-price')
                                                else:
                                                            qs = self.model.objects.filter(name__icontains=nome,tipo_materiale__icontains=material ,price__gte=min_price).order_by('-price')
                                else:
                                                             qs = self.model.objects.filter(name__icontains=nome,tipo_materiale__icontains=material).order_by('-price')

            else:
                        qs= self.model.objects.all()
            return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchView,self).get_context_data(**kwargs)
        context['form'] = SearchForm(initial= {
            'nome': self.request.GET.get('nome'),
            'material': self.request.GET.get('material'),
            'min_price': self.request.GET.get('min_price'),
            'max_price': self.request.GET.get('max_price'),
        })
        return context

@method_decorator([login_required,owner_required],name='dispatch')
class ListaProdFornitore(ListView):
    model = Prodotti
    form_class = Lista_fornitoreForm
    template_name = "products/prodotti_fornitore.html"
    context_object_name = 'prodotti_fornitore'

    def get_queryset(self):
        nome = self.request.GET.get('nome')
        user = self.request.user.username
        categoria = self.request.GET.get('categoria')
        if nome :
            qs = self.model.objects.filter(owner__user__username=user,name__icontains=nome)
        else:
            qs = self.model.objects.filter(owner__user__username=user)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListaProdFornitore, self).get_context_data(**kwargs)
        context['form'] = Lista_fornitoreForm(initial={
            'nome': self.request.GET.get('nome'),

        })
        return context

@method_decorator([login_required,client_required],name='dispatch')
class ListaRevCliente(ListView):
    model = Review
    form_class = Lista_RevForm
    template_name = "products/lista_review.html"
    context_object_name = 'lista_rev'

    def get_queryset(self):
        nome = self.request.GET.get('nome')
        user = self.request.user.username

        if nome:
            qs = self.model.objects.filter(user__user__username=user,prodotto__name=nome )
        else:
            qs = self.model.objects.filter(user__user__username=user)
        return qs
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListaRevCliente, self).get_context_data(**kwargs)
        context['form'] = Lista_RevForm(initial={
            'nome': self.request.GET.get('nome'),

        })
        return context

def product_detail(request, id):
    product = get_object_or_404(Prodotti, id=id, available=True)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'products/products_detail.html', context)