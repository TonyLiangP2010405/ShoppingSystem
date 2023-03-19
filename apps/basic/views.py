from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from apps.basic.forms import ShippingAddressInfo
from apps.basic.models import ShippingAddress
from apps.goods.models import Product, ProductsCategory


# Create your views here.
def home_page(request):
    datas = Product.objects.all().order_by("product_id")
    datas2 = ProductsCategory.objects.all().order_by("category_id")
    p2 = Paginator(datas2, 3)
    p = Paginator(datas, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
        page_obj2 = p2.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
        page_obj2 = p2.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
        page_obj2 = p2.page(p2.num_pages)
    return render(request, "homePage2.html", {"products": page_obj, "categorys": datas2})


def home_page_filter(request):
    datas = Product.objects.all().order_by("price")
    datas2 = ProductsCategory.objects.all().order_by("category_id")
    p = Paginator(datas, 3)
    p2 = Paginator(datas2, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
        page_obj2 = p2.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
        page_obj2 = p2.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
        page_obj2 = p2.page(p.num_pages)
    return render(request, "homePage2.html", {"products": page_obj, "categorys": datas2})


def home_page_filter_desc(request):
    datas = Product.objects.all().order_by("-price")
    datas2 = ProductsCategory.objects.all().order_by("category_id")
    p = Paginator(datas, 3)
    p2 = Paginator(datas2, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
        page_obj2 = p2.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
        page_obj2 = p2.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
        page_obj2 = p2.page(p.num_pages)
    return render(request, "homePage2.html", {"products": page_obj, "categorys": datas2})


def ajax_search(request):
    product_name = request.POST.get("product_name", '')
    url = "/filter_product_name/?name=" + product_name
    return JsonResponse({"url": url})


def filter_category(request):
    category_id = request.GET.get("category_id", '')
    categorys = ProductsCategory.objects.all()
    if category_id:
        datas = Product.objects.filter(category__category_id=category_id).order_by("category_id")
        datas2 = ProductsCategory.objects.all().order_by('category_id')
        p = Paginator(datas, 3)
        p2 = Paginator(datas2, 3)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
            page_obj2 = p2.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
            page_obj2 = p2.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
            page_obj2 = p2.page(p2.num_pages)
        return render(request, "homepage_category_filter.html", {"products": page_obj, "categorys": datas2, "category_id": category_id})
    else:
        datas = Product.objects.all().order_by("product_id")
        datas2 = ProductsCategory.objects.all().order_by('category_id')
        p = Paginator(datas, 3)
        p2 = Paginator(datas2, 3)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
            page_obj2 = p2.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
            page_obj2 = p2.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
            page_obj2 = p2.page(p2.num_pages)
        return render(request, "homePage2.html", {"products": page_obj, "categorys": datas2})


def filter_category_price_homepage(request):
    category_id = request.GET.get("category_id", '')
    datas = Product.objects.filter(category__category_id=category_id).order_by("price")
    datas2 = ProductsCategory.objects.all().order_by("category_id")
    p = Paginator(datas, 3)
    p2 = Paginator(datas2, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
        page_obj2 = p2.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
        page_obj2 = p2.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
        page_obj2 = p2.page(p.num_pages)
    return render(request, "homepage_category_filter.html", {"products": page_obj, "categorys": datas2, "category_id": category_id})


def filter_category_price_homepage_desc(request):
    category_id = request.GET.get("category_id", '')
    datas = Product.objects.filter(category__category_id=category_id).order_by("-price")
    datas2 = ProductsCategory.objects.all().order_by("category_id")
    p = Paginator(datas, 3)
    p2 = Paginator(datas2, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
        page_obj2 = p2.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
        page_obj2 = p2.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
        page_obj2 = p2.page(p.num_pages)
    return render(request, "homepage_category_filter.html", {"products": page_obj, "categorys": datas2, "category_id": category_id})


def ajax_filter_category(request):
    category_id = request.GET.get("category_id", '')
    if len(category_id) != 0:
        return JsonResponse({"url": "/filter_category_name/?category_id="+category_id})
    else:
        return JsonResponse({"error": "error"})

def filter_product(request):
    name = request.GET.get("name", '')
    categorys = ProductsCategory.objects.all()
    if name:
        datas = Product.objects.filter(name__icontains=name).order_by("name")
        datas2 = ProductsCategory.objects.all().order_by('category_id')
        p = Paginator(datas, 3)
        p2 = Paginator(datas2, 3)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
            page_obj2 = p2.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
            page_obj2 = p2.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
            page_obj2 = p2.page(p2.num_pages)
        return render(request, "homePage2.html", {"products": page_obj, "categorys": datas2})
    else:
        datas = Product.objects.all().order_by("product_id")
        datas2 = ProductsCategory.objects.all().order_by('category_id')
        p = Paginator(datas, 3)
        p2 = Paginator(datas2, 3)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
            page_obj2 = p2.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
            page_obj2 = p2.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
            page_obj2 = p2.page(p2.num_pages)
        return render(request, "homePage2.html", {"products": page_obj, "categorys": datas2})


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

