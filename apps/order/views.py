from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from apps.goods.models import Product
from apps.order.models import ShoppingCart, Order, OrderList
from apps.users.models import MyUser
from apps.basic.models import ShippingAddress


# Create your views here.
def show_shopping_cart(request):
    if request.user.is_authenticated:
        shopping_carts = ShoppingCart.objects.filter(user=MyUser.objects.filter(username=request.user.username)[0])
        total_amount = 0
        total_number = 0
        for shopping_cart in shopping_carts:
            total_amount += shopping_cart.count_number * shopping_cart.product.price
            total_number += shopping_cart.count_number
        return render(request, "ShoppingCart.html", {"shopping_cart": shopping_carts, "total_number": total_number, "total_amount": total_amount})
    else:
        return redirect('login')


def ajax_shopping_cart_data(request):
    if request.user.is_authenticated:
        product_id = request.POST.get("product_id", "")
        shopping_cart = ShoppingCart.objects.filter(product_id=product_id,
                                                    user=MyUser.objects.filter(username=request.user.username)[0])
        if shopping_cart:
            count_number = shopping_cart[0].count_number
            json_dict = {"code": 0, "warning": "The product has been exist"}
        else:
            product = Product.objects.filter(product_id=product_id)[0]
            ShoppingCart.objects.create(product=product, count_number=1,
                                        user=MyUser.objects.filter(username=request.user.username)[0])
            count_number = 1
            json_dict = {"code": 0, "msg": "Add shoppingCart successful"}
        return JsonResponse(json_dict)
    else:
        product_id = request.POST.get("product_id", "")
        json_dict = {"code": 1, "msg": "You are not login, redirect to login page",
                     'url': '/shoppingCart/user_login/' + product_id}
        return JsonResponse(json_dict)


def shopping_cart_ajax_delete(request):
    shopping_cart_id = request.POST.get("shopping_cart_id", "")
    ShoppingCart.objects.filter(shopping_cart_id=shopping_cart_id,
                                user=MyUser.objects.filter(username=request.user.username)[0]).delete()
    json_dict = {"code": 1000, "msg": "delete successful"}
    return JsonResponse(json_dict)


def user_shopping_cart_login(request, product_id):
    return render(request, "user_shoppingCart_login2.html", {"product_id": product_id})


def shopping_cart_ajax_minus(request):
    count_number = request.POST.get("count", '')
    int_count_number = int(count_number)
    if int_count_number > 1:
        shopping_cart_id = request.POST.get("shopping_cart_id", '')
        shopping_cart = ShoppingCart.objects.filter(shopping_cart_id=shopping_cart_id,
                                                    user=MyUser.objects.filter(username=request.user.username)[0])[0]
        shopping_cart.count_number = int_count_number - 1
        shopping_cart.save()
        data = {"msg": "success"}
    else:
        data = {"warning": "the count number cannot be less than one"}
    return JsonResponse(data)


def shopping_cart_ajax_plus(request):
    count_number = request.POST.get("count", '')
    int_count_number = int(count_number)
    shopping_cart_id = request.POST.get("shopping_cart_id", '')
    shopping_cart = ShoppingCart.objects.filter(shopping_cart_id=shopping_cart_id,
                                                user=MyUser.objects.filter(username=request.user.username)[0])[0]
    shopping_cart.count_number = int_count_number + 1
    shopping_cart.save()
    data = {"msg": "success"}
    return JsonResponse(data)


def ajax_login_data(request):
    product_id = request.POST.get("product_id", '')
    uname = request.POST.get("username", '')
    pwd = request.POST.get("password", '')
    json_dict = {}
    if uname != '' and pwd != '':
        if len(MyUser.objects.filter(username=uname)) != 0:
            user = authenticate(username=uname, password=pwd)
            if user:
                if user.is_active:
                    login(request, user)
                    json_dict["code"] = 1000
                    json_dict["msg"] = "login successful"
                    json_dict["url"] = '/products/customer/' + product_id
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


def show_purchase_order(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=MyUser.objects.filter(username=request.user.username)[0]).order_by(
            "-purchase_date")
        print(orders)
        if len(orders) != 0:
            return render(request, "purchase_order.html", {"orders": orders})
        return render(request, "purchase_order.html")
    else:
        return render(request, "purchase_order.html")


def add_purchase_order(request):
    orders = Order.objects.filter(user=MyUser.objects.filter(username=request.user.username)[0])
    order_lists = OrderList.objects.all()
    print(order_lists)
    order_id = order_lists[0].order_id
    product_json = {}
    product_list = []
    if len(order_lists) != 0:
        total_order_amount = 0
        for order_list in order_lists:
            total_order_amount = order_list.total_price + total_order_amount
            order_lists[0].order.total_order_amount = total_order_amount
        if len(orders) != 0:
            for i in range(len(order_lists)):
                product_list.append(order_lists[i].product.product_id)
            product_json["product_id_list"] = product_list
            order = orders[len(orders) - 1]
            order.total_order_amount = total_order_amount
            order.purchase_date = timezone.now()
            order.product_json = product_json
            order.save()
            order_lists.delete()
    return redirect('/purchase_order/order_detail/' + str(order_id))


def show_order_list(request):
    order_lists = OrderList.objects.all()
    return render(request, "order_list.html", {"order_lists": order_lists})


def add_order_list(request):
    status = False
    if len(ShoppingCart.objects.all()) != 0:
        total_price = 0
        total_number = 0
        count_number = 0
        price = 0
        shopping_carts = ShoppingCart.objects.filter(user=MyUser.objects.filter(username=request.user.username)[0])
        user = MyUser.objects.filter(username=request.user.username)[0]
        if len(Order.objects.filter(user=user)) == 0 or Order.objects.filter(user=user)[
            len(Order.objects.filter(user=user)) - 1].total_order_amount != 0:
            Order(purchase_order_status="pending", total_order_amount="0", user=user).save()
            orders = Order.objects.all()
            order = orders[len(orders) - 1]
        else:
            order = Order.objects.filter(user=user)[len(Order.objects.filter(user=user)) - 1]
        for shopping_cart in shopping_carts:
            order_lists = OrderList.objects.all()
            if len(order_lists) != 0:
                for order_list in order_lists:
                    total_price = order_list.total_price
                    total_number = order_list.total_number
            check_order_list = OrderList.objects.filter(product=shopping_cart.product)
            if len(check_order_list) == 0:
                order_list_product = shopping_cart.product
                order_list_product_count = shopping_cart.count_number
                count_number = order_list_product_count + count_number
                shopping_cart.product.sale_number = shopping_cart.count_number
                shopping_cart.product.save()
                product_price = order_list_product.price * order_list_product_count
                shopping_cart.product.sale_amount = shopping_cart.count_number * shopping_cart.product.price
                shopping_cart.product.save()
                print(product_price)
                price = product_price + price
                total_price = price
                total_number = total_number + order_list_product_count
                OrderList.objects.create(total_price=product_price, total_number=order_list_product_count,
                                         product=order_list_product,
                                         order=order)
            else:
                check_order_list[0].total_number += shopping_cart.count_number
                check_order_list[0].total_price += shopping_cart.count_number * shopping_cart.product.price
                shopping_cart.product.sale_number = check_order_list[0].total_number
                shopping_cart.product.sale_amount = check_order_list[0].total_price
                check_order_list[0].save()
                status = True
            shopping_cart.delete()
        if status:
            total_price = 0
            total_number = 0
            for order_list in OrderList.objects.all():
                total_price += order_list.total_price
                total_number += order_list.total_number
            status = False
        order_lists = OrderList.objects.all()
        return render(request, "order_list.html", {"order_lists": order_lists, "total_price": total_price,
                                                   "count_number": total_number})
    else:
        return render(request, "order_list.html")


def show_order_detail(request, order_id):
    total_quantity = 0
    order = Order.objects.filter(order_id=order_id)[0]
    product_id_list = order.product_json["product_id_list"]
    product_list = []
    shipped_address = ShippingAddress.objects.filter(user=order.user)[0]
    for product_id in product_id_list:
        product = Product.objects.filter(product_id=product_id)[0]
        total_quantity += product.sale_number
        product_list.append(product)
    return render(request, 'order_detail.html', {"order": order, "product_list": product_list, "address": shipped_address, "total_quantity": total_quantity})


def filter_order_ajax(request):
    group = request.POST.get('group', '')
    print(group)
    if int(group) == 1:
        orders = Order.objects.filter(purchase_order_status="pending" or "hold").order_by("-purchase_date")
        order_list = []
        for order in orders:
            order_list.append(order)
        json_dict = {"orders": order_list}
        print(json_dict)
        return JsonResponse(json_dict)
    if group == 2:
        orders = Order.objects.filter(purchase_order_status="shipped" or "cancelled").order_by("-purchase_data")
        order_list = []
        for order in orders:
            order_list.append(order)
        json_dict = {"orders": order_list}
        print(json_dict)
        return JsonResponse(json_dict)
    return JsonResponse({"error": "error"})


def order_check_user_ajax(request):
    order_id = request.POST.get("order_id", '')
    order = Order.objects.filter(order_id=order_id)[0]
    if request.user.is_superuser:
        order.cancel_user_type = 'vendor'
        order.cancelDate = timezone.now()
        order.purchase_order_status = 'cancelled'
        order.save()
    else:
        order.cancel_user_type = 'customer'
        order.cancelDate = timezone.now()
        order.purchase_order_status = 'cancelled'
        order.save()
    return JsonResponse({"msg": "success"})


def get_order_quantity(request):
    order_quantity = Order.objects.all().count()
    print(order_quantity)
    return JsonResponse({"order_quantity": order_quantity})


def show_vendor_order(request):
    orders = Order.objects.all().order_by("-purchase_date")
    return render(request, "purchase_order.html", {"orders": orders})


def ajax_shipped(request):
    order_id = request.POST.get("order_id", '')
    order = Order.objects.filter(order_id=order_id)[0]
    order.purchase_order_status = "shipped"
    order.shipped_date = timezone.now()
    order.save()
    return JsonResponse({"msg": "success"})


def ajax_search(request):
    order_id = request.POST.get("order_id", '')
    print(order_id)
    if order_id == '':
        return JsonResponse({"msg": "reload"})
    else:
        order = Order.objects.filter(order_id=order_id)
        if len(order) != 0:
            return JsonResponse({"msg": "success"})
        else:
            return JsonResponse({"msg": "fail"})


def ajax_hold(request):
    order_id = request.POST.get("order_id", '')
    order = Order.objects.filter(order_id=order_id)[0]
    order.purchase_order_status = "hold"
    order.save()
    return JsonResponse({"msg": "success"})


def ajax_unhold(request):
    order_id = request.POST.get("order_id", '')
    order = Order.objects.filter(order_id=order_id)[0]
    order.purchase_order_status = "shipped"
    order.shipped_date = timezone.now()
    order.save()
    return JsonResponse({"msg": "success"})


def filter_order_pending(request):
    orders = Order.objects.filter(purchase_order_status='pending').order_by("-purchase_date")
    return render(request, 'order_filter_pending.html', {'orders': orders})


def filter_order_hold(request):
    orders = Order.objects.filter(purchase_order_status='hold').order_by("-purchase_date")
    return render(request, 'order_filter_hold.html', {'orders': orders})


def filter_order_current(request):
    orders = Order.objects.filter(user=MyUser.objects.filter(username=request.user.username)[0], purchase_order_status='pending') | Order.objects.filter(user=MyUser.objects.filter(username=request.user.username)[0],
        purchase_order_status='hold').order_by("-purchase_date")
    return render(request, 'order_filter_current.html', {"orders": orders})


def filter_order_past(request):
    if request.user.is_superuser:
        orders = Order.objects.filter(purchase_order_status='cancelled') | Order.objects.filter(
            purchase_order_status='shipped').order_by("-purchase_date")
    else:
        orders = Order.objects.filter(user=MyUser.objects.filter(username=request.user.username)[0],purchase_order_status='cancelled') | Order.objects.filter(
            user=MyUser.objects.filter(username=request.user.username)[0], purchase_order_status='shipped').order_by("-purchase_date")
    return render(request, 'order_filter_past.html', {"orders": orders})


def back_shopping_cart(request):
    order_lists = OrderList.objects.all()
    shopping_cart_checks = ShoppingCart.objects.all()
    for order_list in order_lists:
        if len(shopping_cart_checks) != 0:
            for shopping_cart_check in shopping_cart_checks:
                if order_list.product.product_id == shopping_cart_check.product.product_id:
                    shopping_cart_check.count_number += order_list.total_number
                    shopping_cart_check.save()
                else:
                    ShoppingCart.objects.create(product=order_list.product, count_number=order_list.total_number, user=MyUser.objects.filter(username=request.user.username)[0])
        else:
            ShoppingCart.objects.create(product=order_list.product, count_number=order_list.total_number,
                                        user=MyUser.objects.filter(username=request.user.username)[0])
        order_list.delete()
    return redirect('shopping_cart')