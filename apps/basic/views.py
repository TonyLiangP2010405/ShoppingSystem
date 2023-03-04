from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from apps.basic.forms import ShippingAddressInfo
from apps.basic.models import ShippingAddress
from apps.goods.models import Product


# Create your views here.
def home_page(request):
    datas = Product.objects.all().order_by("price")
    p = Paginator(datas, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, "homePage.html", {"products": page_obj})


def home_page_filter(request):
    datas = Product.objects.all().order_by("category_id")
    p = Paginator(datas, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, "homePage.html", {"products": page_obj})


def ajax_search(request):
    product_name = request.POST.get("product_name", '')
    url = "/filter_product_name/?name="+ product_name
    return JsonResponse({"url": url})


def filter_product(request):
    name = request.GET.get("name", '')
    if name:
        datas = Product.objects.filter(name=name).order_by("price")
        p = Paginator(datas, 5)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        return render(request, "homePage.html", {"products": page_obj})
    else:
        datas = Product.objects.all().order_by("product_id")
        p = Paginator(datas, 5)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        return render(request, "homePage.html", {"products": page_obj})


def add_shipping_address(request):
    if request.method == "GET":
        form_obj = ShippingAddressInfo()
        return render(request, "add_shippingAddress.html", {"form_obj": form_obj})
    if request.method == "POST":
        form_obj = ShippingAddressInfo(request.POST, request.FILES)
        if form_obj.is_valid():
            shipping_address_dict = {}
            user = request.user
            receiver_name = request.POST.get("receiver_name", '')
            receiver_phone = request.POST.get("receiver_phone", '')
            receiver_mobile = request.POST.get("receiver_mobile", '')
            receiver_province = request.POST.get("receiver_province", '')
            receiver_city = request.POST.get("receiver_city", '')
            receiver_district = request.POST.get("receiver_district", '')
            receiver_address = request.POST.get("receiver_address", '')
            receiver_zip = request.POST.get("receiver_zip", '')
            shipping_address_dict["user"] = user
            shipping_address_dict["receiver_name"] = receiver_name
            shipping_address_dict["receiver_phone"] = receiver_phone
            shipping_address_dict["receiver_mobile"] = receiver_mobile
            shipping_address_dict["receiver_province"] = receiver_province
            shipping_address_dict["receiver_city"] = receiver_city
            shipping_address_dict["receiver_district"] = receiver_district
            shipping_address_dict["receiver_address"] = receiver_address
            shipping_address_dict["receiver_zip"] = receiver_zip
            ShippingAddress.objects.create(**shipping_address_dict)
    return redirect("homePage")
