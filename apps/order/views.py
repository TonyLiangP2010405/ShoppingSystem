from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from apps.order.models import ShoppingCart
from apps.goods.models import Product
from apps.users.models import MyUser
from django.contrib.sessions.backends.db import SessionStore

# Create your views here.
def show_shopping_cart(request):
    shopping_cart = ShoppingCart.objects.all()
    return render(request, "ShoppingCart.html", {"shopping_cart": shopping_cart})


def ajax_shopping_cart_data(request):
    if request.user.is_authenticated:
        product_id = request.POST.get("product_id", "")
        shopping_cart = ShoppingCart.objects.filter(product_id=product_id)
        if shopping_cart:
            shopping_cart[0].count_number = shopping_cart[0].count_number + 1
            count_number = shopping_cart[0].count_number
            shopping_cart[0].save()
            json_dict = {"code": 0, "msg": "Add shoppingCart successful"}
        else:
            product = Product.objects.filter(product_id=product_id)[0]
            ShoppingCart.objects.create(product=product, count_number=1)
            count_number = 1
            json_dict = {"code": 0, "msg": "Add shoppingCart successful"}
        if "shopping_cart" in request.session:
            request.session["shopping_cart"] = {"product_id": product_id, "count_number": count_number}
            request.session.save()
            print(request.session)
            print('test1')
        else:
            s = SessionStore()
            s["shopping_cart"] = {"product_id": product_id, "count_number": count_number}
            s.create()
            print(s)
            print('test2')
        return JsonResponse(json_dict)
    else:
        json_dict = {"code": 1, "msg": "You are not login, redirect to login page", 'url': '/user_login/'}
        return JsonResponse(json_dict)


def shopping_cart_ajax_delete(request):
    shopping_cart_id = request.POST.get("shopping_cart_id", "")
    ShoppingCart.objects.filter(shopping_cart_id=shopping_cart_id).delete()
    json_dict = {"code": 1000, "msg": "delete successful"}
    return JsonResponse(json_dict)


def user_shopping_cart_login(request, product_id):
    return render(request, "user_shoppingCart_login.html", {"product_id": product_id})


def ajax_login_data(request):
    if "shopping_cart" in request.session:
        shopping_cart = request.session.get("shopping_cart")
        print(shopping_cart)
        product = Product.objects.filter(product_id=shopping_cart["product_id"])
        count_number = shopping_cart["count_number"]
        ShoppingCart.objects.create(product=product, count_number=count_number)
    product_id = request.POST.get("product_id", '')
    uname = request.POST.get("username", '')
    pwd = request.POST.get("password", '')
    json_dict = {}
    if uname and pwd:
        if MyUser.objects.filter(username=uname):
            user = authenticate(username=uname, password=pwd)
            if user:
                if user.is_active:
                    login(request, user)
                    json_dict["code"] = 1000
                    json_dict["msg"] = "login successful"
                    json_dict["url"] = '/products/customer/' + product_id
                    print(json_dict)
                else:
                    json_dict["code"] = 1001
                    json_dict["msg"] = "the user doesn't active"
            else:
                json_dict["code"] = 1002
                json_dict["msg"] = "the password is wrong, please try again"
        else:
            json_dict["code"] = 1003
            json_dict["msg"] = "the username is wrong, please try again"
    else:
        json_dict["code"] = 1004
        json_dict["msg"] = "the username or password is empty"
    return JsonResponse(json_dict)
