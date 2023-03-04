from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from apps.goods.models import Product
from apps.basic.models import ShippingAddress
from apps.users.forms import UserRegForm, UserChangePasswordForm
from apps.users.models import MyUser
from django.contrib.auth.hashers import make_password
from apps.basic.forms import ShippingAddressInfo
from apps.order.models import ShoppingCart



# Create your views here.
def user_register(request):
    if request.method == "GET":
        form_obj = UserRegForm()
        form_obj2 = ShippingAddressInfo()
        return render(request, 'user_register.html', {'form_obj': form_obj, 'form_obj2': form_obj2})
    if request.method == "POST":
        form_obj = UserRegForm(request.POST, request.FILES)
        form_obj2 = ShippingAddressInfo(request.POST, request.FILES)
        if form_obj.is_valid() and form_obj2.is_valid():
            uname = request.POST.get("username", '')
            users = MyUser.objects.filter(username=uname)
            email = request.POST.get("email", '')
            password = request.POST.get("password", '')
            if users:
                info = 'the user has been existed'
                return render(request, 'user_register.html',
                              {"form_obj": form_obj, 'form_obj2': form_obj2, "info": info})
            else:
                form_obj.cleaned_data["username"] = uname
                form_obj.cleaned_data["email"] = email
                form_obj.cleaned_data.pop("re_password")
                form_obj.cleaned_data["is_staff"] = 1
                form_obj.cleaned_data["is_superuser"] = 0
                # new user
                MyUser.objects.create_user(**form_obj.cleaned_data)
                form_obj2 = ShippingAddressInfo(request.POST, request.FILES)
                shipping_address_dict = {}
                receiver_name = request.POST.get("receiver_name", '')
                receiver_phone = request.POST.get("receiver_phone", '')
                receiver_mobile = request.POST.get("receiver_mobile", '')
                receiver_province = request.POST.get("receiver_province", '')
                receiver_city = request.POST.get("receiver_city", '')
                receiver_district = request.POST.get("receiver_district", '')
                receiver_address = request.POST.get("receiver_address", '')
                receiver_zip = request.POST.get("receiver_zip", '')
                shipping_address_dict["receiver_name"] = receiver_name
                shipping_address_dict["receiver_phone"] = receiver_phone
                shipping_address_dict["receiver_mobile"] = receiver_mobile
                shipping_address_dict["receiver_province"] = receiver_province
                shipping_address_dict["receiver_city"] = receiver_city
                shipping_address_dict["receiver_district"] = receiver_district
                shipping_address_dict["receiver_address"] = receiver_address
                shipping_address_dict["receiver_zip"] = receiver_zip
                user_login = authenticate(username=uname, password=password)
                login(request, user_login)
                user = request.user
                shipping_address_dict["user"] = user
                ShippingAddress.objects.create(**shipping_address_dict)
                return redirect("homePage")
        else:
            errors = form_obj.errors
            print(errors)
            return render(request, "user_register.html",
                          {'form_obj': form_obj, 'form_obj2': form_obj2, 'errors': errors})


def user_login(request):
    return render(request, "user_login.html")


def ajax_login_data(request):
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


def user_logout(request):
    if request.user.is_authenticated:
        return render(request, "user_logout.html")
    else:
        return redirect('login')


def ajax_logout_data(request):
    json_dict = {}
    logout(request)
    json_dict["code"] = 1000
    json_dict["msg"] = "logout successful, please waite 3 seconds"
    return JsonResponse(json_dict)


def change_password(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            form_obj = UserChangePasswordForm()
            return render(request, "change_password.html", {'form_obj': form_obj})
        if request.method == "POST":
            form_obj = UserChangePasswordForm(request.POST, request.FILES)
            if form_obj.is_valid():
                uname = request.user.username
                original_password = request.POST.get("original_password", '')
                new_password = request.POST.get("new_password", '')
                users = MyUser.objects.filter(username=uname)
                for user in users:
                    if user.username == uname and user.check_password(original_password):
                        MyUser.objects.filter(username=uname).update(password=make_password(new_password))
                        info = 'You have changed password successful'
                        return render(request, 'change_password_successful.html', {"info": info})
                    else:
                        info = 'the original password has some problem'
                        return render(request, "change_password.html", {'info': info})
            else:
                errors = form_obj.errors
                print(errors)
                return render(request, "change_password_fail.html", {'errors': errors})
