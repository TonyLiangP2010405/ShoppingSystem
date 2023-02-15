from django.urls import path
from apps.order import views


urlpatterns = [
    path('shoppingCart/', views.show_shopping_cart, name="shopping_cart"),
    path('shoppingCart/ajax_shopping_cart_data/', views.ajax_shopping_cart_data),
    path('shoppingCart/ajax_delete', views.shopping_cart_ajax_delete),
    path('shoppingCart/user_login/<int:product_id>', views.user_shopping_cart_login, name='login2'),
    path('shoppingCart/user_login/ajax_login_data/', views.ajax_login_data),
]
