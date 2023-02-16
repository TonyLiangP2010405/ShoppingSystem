from django.urls import path
from apps.order import views


urlpatterns = [
    path('shoppingCart/', views.show_shopping_cart, name="shopping_cart"),
    path('shoppingCart/ajax_shopping_cart_data/', views.ajax_shopping_cart_data),
    path('shoppingCart/ajax_delete', views.shopping_cart_ajax_delete),
    path('shoppingCart/user_login/<int:product_id>', views.user_shopping_cart_login, name='login2'),
    path('shoppingCart/user_login/ajax_login_data/', views.ajax_login_data),
    path('purchase_order/', views.add_purchase_order, name='add_order'),
    path('order_list/', views.add_order_list, name='add_order_list'),
    path('show_purchase_order/', views.show_purchase_order, name='show_order'),
    path('show_order_list', views.show_order_list, name='show_order_list'),
    path('purchase_order/order_detail/<int:order_id>', views.show_order_detail, name='order_detail'),
    path('shoppingCart/ajax_minus/', views.shopping_cart_ajax_minus),
    path('shoppingCart/ajax_plus/', views.shopping_cart_ajax_plus),
]
