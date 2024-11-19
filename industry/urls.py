"""
URL configuration for industry project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('checkout/', views.checkout, name='checkout'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('search/', views.search, name='search'),

    path('product/<str:categories>/', views.productdisplay, name='product_display'),
    path('product/details/<int:myid>', views.productview, name='product_detail'),

    path('placeorder/', views.placeorder, name='home'),

    path('cart/', views.cart, name='cart'),
    path('add_cart/<int:product_number>', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_number>', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_number>', views.remove_cart_item, name='remove_cart_item'),



    path('login/', views.loginaction, name='login'),
    path('register/', views.signaction, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
