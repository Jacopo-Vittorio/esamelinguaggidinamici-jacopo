from django.urls import path


from products import views

from .views import SearchView, ProdottiList, ProdottiCreate, ProdottiDelete, ProdottiUpdate, ListaProdFornitore, \
    ListaRevCliente, RevDelete

app_name = 'prod'

urlpatterns = [
    path('products/<int:pk>/detail',views.product_related,name='products-detail'),
    path('products/<int:pk>/list', ProdottiList.as_view(), name='products-list'),
    path('products/create',ProdottiCreate.as_view(), name='products-create'),
    path('products/<int:pk>/delete',ProdottiDelete.as_view(),name = 'products-delete'),
    path('products/<int:pk>/update',ProdottiUpdate.as_view(),name = 'products-update'),
    path('categoria/',views.CategoriaView,name = 'products-category'),
    path('product/<int:pk>/recensioni', views.add_review, name='products-review'),
    path('newcat',views.ReportView.as_view(),name='report_newcat'),
    path('',SearchView.as_view() , name='search'),
    path('gestioneprodotti',ListaProdFornitore.as_view(),name='gestione-prodotti'),
    path('<int:pk>/eliminazione',RevDelete.as_view(),name='remove-review'),
    path('listaReview',ListaRevCliente.as_view(),name='lista-review')

]