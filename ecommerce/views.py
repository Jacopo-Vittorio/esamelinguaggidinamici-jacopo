import logging

from django.contrib.auth.forms import UserCreationForm
from django.http import  HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from products.recommendations import get_suggested_products

_logger = logging.getLogger(__name__)

def maintenance(request,cheneso):
    _logger.warning(request)
    return HttpResponse(f"Tutto ok {cheneso}")

class Maintenance(TemplateView):
    template_name = 'Maintenance.html'

class NotFound(TemplateView):

    template_name = '404.html'

class Homepage(TemplateView):

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suggested_products'] = get_suggested_products(self.request.user)
        return context

class UserCreationView(CreateView):
    form_class = UserCreationForm  #creata un anuova view per la creazione utente
    template_name = '../user_manage/templates/user_manage/registration/user_creation.html'  #creo il templates che non sarà diverso dal templateform vecchi
    success_url =  reverse_lazy('homepage')
