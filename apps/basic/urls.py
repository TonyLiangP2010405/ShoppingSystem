from django.contrib import admin
from django.urls import path, include
from apps.basic import views

urlpatterns = [
    path('', views.home_page, name='homePage'),
    path('user/add_shipping_address/', views.add_shipping_address, name='add_shipping_address'),
    path('filter/', views.home_page_filter, name='homePage_filter'),
    path('ajax_search/', views.ajax_search),
    path('filter_product_name/', views.filter_product, name='filter_product_name'),
    path('ajax_search2/', views.ajax_search2),
    path('filter_category_name/', views.filter_category, name='filter_category_name')
]