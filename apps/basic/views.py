from django.shortcuts import render, redirect
from apps.basic.forms import ShippingAddressInfo
from apps.basic.models import ShippingAddress


# Create your views here.
def home_page(request):
    return render(request, "homePage.html")


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
