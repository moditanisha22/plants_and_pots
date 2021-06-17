"""plants_and_pots URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
app_name='pots'
urlpatterns = [
    path('',views.index.as_view(),name='index'),
    path('pot_detail/<slug:slug>/<int:pk>',views.Pot_Detail,name='pot_detail'),
    path('add_to_cart/<slug:slug>',views.AddtoCart,name='addcart'),
    path('cart_list/',views.CartList.as_view(),name='cart_list'),
    path('increse_quantity/<slug:slug>',views.increse_quantity,name='increase'),
    path('decrease/<slug:slug>/',views.decrese_quantity,name='decrease'),
    path('delete_cart_pot/<slug:slug>',views.delete_pot,name='delete_cart_pot'),
    path('quick_shop_checkout/<slug:slug>/',views.quick_shop_checkout,name='quick_shop_checkout'),
    path('quick_increse_quantity/<slug:slug>/<int:pk>',views.quick_increse_quantity,name='quick_increase'),
    path('quick_decrease/<slug:slug>/<int:pk>',views.quick_decrese_quantity,name='quick_decrease'),
    path('checkout/',views.final_checkout,name='checkout'),
    path('quick_checkout/<int:pk>',views.quick_checkout,name='quick_checkout'),
    path('quick_final_response/',views.quick_final_response,name='quick_final_response'),
    path('quick_fial_order/<int:pk>/',views.quick_final_order,name='quick_final_order'),
    path('fianl_order/',views.final_order,name='final_order'),
    path('myorder/',views.myorder,name='myorder'),
    path('all_product/', views.all_product.as_view(), name='all_product'),
    path('search_product/<str:category>/',views.search_category,name='search_product'),
    path('add_address/',views.add_address,name='add_address'),
    path('delete_address/<int:pk>',views.delete_address,name='delete_address'),
    path('create_order/',views.create_order,name='create_order'),
    path('final_response/',views.final_response,name='final_response'),
    path('quick_create_order/<int:pk>/',views.quick_create_order,name='quick_create_order'),
    
    
]
