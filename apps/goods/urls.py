from django.urls import path
from apps.goods import views


urlpatterns = [
    path('', views.vendor_product_view, name='products'),
    path('customer/<int:product_id>/', views.product_detail, name="product_detail"),
    path('ajax_products/', views.ajax_products),
    path('add_product/', views.product_add, name='add_product'),
    path('customer/', views.user_product_view, name='user_products')
]

