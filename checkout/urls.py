from django.urls import  path
from . import views

app_name = 'order'

urlpatterns = [
    path('create/',views.OrderCreateView.as_view(),name='order_create'),
    path('gestione_ordini', views.ListaRichieste.as_view(),name='order-list'),
    path('dettaglio_ordine/<int:pk>', views.DetailOrder.as_view(),name='order-detail'),
    path('delete_prod_order/<int:pk>', views.DeleteOrder.as_view(),name='order-delete'),
]