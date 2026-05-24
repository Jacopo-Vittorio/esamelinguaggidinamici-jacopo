import views
from django.urls import path



from .views import ThreadCreate, ThreadList, RispostaList,AddComment

app_name ='forum'

urlpatterns = [
    path('create',ThreadCreate.as_view(), name='thread-create'),
    path('list/',ThreadList.as_view(),name='thread-list'),
    path('forum/<int:pk>/discussione/', RispostaList.as_view(),name='discussione'),
    path('forum/<int:pk>/creacommento/',AddComment.as_view(),name='crea-commento')

    ]