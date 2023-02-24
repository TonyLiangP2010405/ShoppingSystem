from django.conf.urls.static import static
from django.urls import path
from apps.goods import views
from shoppingSystem import settings

urlpatterns = [
    path('', views.vendor_product_view, name='products'),
    path('customer/<int:product_id>/', views.product_detail, name="product_detail"),
    path('ajax_products/', views.ajax_products),
    path('add_product/', views.product_add, name='add_product'),
    path('customer/', views.user_product_view, name='user_products'),
    path('product_change/<int:product_id>', views.product_change, name='product_change'),
    path('product_delete/<int:product_id>', views.product_delete, name='product_delete'),
    path('change_photo/<int:product_id>', views.product_change_photo, name='product_change_photo'),
    path('ajax_change_photo/', views.product_ajax_photo_change),
    path('categories/', views.get_category, name="category"),
    path('categories/<int:category_id>', views.get_category_detail, name="category_detail"),
    path('categories/add_categories', views.add_categories, name="add_category"),
]

