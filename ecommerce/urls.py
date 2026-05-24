"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from ecommerce.views import Maintenance, maintenance, NotFound, Homepage
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('account/', include('django.contrib.auth.urls')),
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('user_manage/', include('user_manage.urls')),
    path('forum/',include('forum.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('order/',include('checkout.urls',namespace='order'))
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
